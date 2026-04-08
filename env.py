"""
env.py — Core Fraud Detection OpenEnv Environment.

Implements the full OpenEnv interface:
  - reset() → FraudObservation
  - step(action) → StepResult
  - state() → EnvironmentState

Supports dynamic difficulty adjustment and adaptive sample selection.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

from models import (
    FraudObservation,
    FraudAction,
    FraudReward,
    StepResult,
    EnvironmentState,
    ExtractedFeatures,
)
from features import extract_features
from reward_engine import compute_reward
from grader import run_grader
from tasks import ALL_TASKS

SAFE = 0
FRAUD = 1
SUSPICIOUS = 2


class FraudDetectionEnv:
    """
    Fraud Detection OpenEnv Environment.

    An agent receives a message / transaction description and must classify it
    as Safe (0), Fraud (1), or Suspicious (2).

    Supports three tasks with increasing difficulty:
        - easy_fraud_detection
        - medium_risk_analysis
        - hard_decision_making
    """

    SUPPORTED_TASKS = list(ALL_TASKS.keys())

    def __init__(self, task_name: str = "easy_fraud_detection") -> None:
        if task_name not in ALL_TASKS:
            raise ValueError(
                f"Unknown task '{task_name}'. Choose from: {self.SUPPORTED_TASKS}"
            )
        self._task_name = task_name
        self._task_config = ALL_TASKS[task_name]
        self._samples: List[Dict[str, Any]] = self._task_config["samples"]

        # Runtime state — initialized by reset()
        self._step_count: int = 0
        self._sample_index: int = 0
        self._action_history: List[int] = []
        self._reward_history: List[float] = []
        self._episode_history: List[Dict[str, Any]] = []
        self._done: bool = False
        self._cumulative_reward: float = 0.0
        self._correct_count: int = 0
        self._consecutive_correct: int = 0
        self._consecutive_wrong: int = 0
        self._suspicious_count: int = 0
        self._rolling_accuracy: float = 0.0
        self._current_observation: Optional[FraudObservation] = None

    # ── Public API ────────────────────────────────────────────────────────────

    def reset(self) -> FraudObservation:
        """
        Reset the environment to its initial state.

        Returns the first observation (first sample in the task).
        """
        self._step_count = 0
        self._sample_index = 0
        self._action_history = []
        self._reward_history = []
        self._episode_history = []
        self._done = False
        self._cumulative_reward = 0.0
        self._correct_count = 0
        self._consecutive_correct = 0
        self._consecutive_wrong = 0
        self._suspicious_count = 0
        self._rolling_accuracy = 0.0

        self._current_observation = self._build_observation()
        return self._current_observation

    def step(self, action: FraudAction) -> StepResult:
        """
        Apply agent action and advance the environment by one step.

        Args:
            action: FraudAction with action ∈ {0, 1, 2}.

        Returns:
            StepResult(observation, reward, done, info)
        """
        if self._done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")

        current_sample = self._samples[self._sample_index]
        label = current_sample["label"]
        act = action.action

        # Compute reward
        reward: FraudReward = compute_reward(
            action=act,
            label=label,
            action_history=self._action_history,
            reward_history=self._reward_history,
        )

        # Update history
        self._action_history.append(act)
        self._reward_history.append(reward.total)
        self._episode_history.append({"action": act, "label": label})
        self._cumulative_reward += reward.total
        self._step_count += 1

        # Track accuracy metrics
        if reward.correct:
            self._correct_count += 1
            self._consecutive_correct += 1
            self._consecutive_wrong = 0
        else:
            self._consecutive_correct = 0
            self._consecutive_wrong += 1

        if act == SUSPICIOUS:
            self._suspicious_count += 1

        # Rolling accuracy (last 10 steps)
        window = self._action_history[-10:]
        labels_window = [
            self._samples[max(0, self._sample_index - len(window) + i)]["label"]
            for i in range(len(window))
        ]
        correct_in_window = sum(
            1 for a, l in zip(window, labels_window) if a == l
        )
        self._rolling_accuracy = correct_in_window / len(window) if window else 0.0

        # Advance sample index
        self._sample_index += 1
        done = self._sample_index >= len(self._samples)
        self._done = done

        # Next observation (or terminal)
        if not done:
            next_obs = self._build_observation()
        else:
            # Terminal observation mirrors last sample's structure
            next_obs = self._current_observation.model_copy(
                update={
                    "step_count": self._step_count,
                    "action_history": list(self._action_history),
                    "reward_history": list(self._reward_history),
                }
            )
        self._current_observation = next_obs

        # Build info dict
        grader_result = None
        if done:
            grader_result = run_grader(self._episode_history, self._task_config)

        info: Dict[str, Any] = {
            "step": self._step_count,
            "label": label,
            "correct": reward.correct,
            "partial": reward.partial,
            "cumulative_reward": round(self._cumulative_reward, 4),
            "rolling_accuracy": round(self._rolling_accuracy, 4),
            "explanation": reward.explanation,
        }
        if grader_result:
            info["grader_result"] = grader_result.model_dump()

        return StepResult(
            observation=next_obs,
            reward=reward,
            done=done,
            info=info,
        )

    def state(self) -> EnvironmentState:
        """Return the full current environment state snapshot."""
        return EnvironmentState(
            task_name=self._task_name,
            difficulty=self._task_config["difficulty"],
            step_count=self._step_count,
            max_steps=len(self._samples),
            current_sample_index=self._sample_index,
            total_samples=len(self._samples),
            cumulative_reward=round(self._cumulative_reward, 4),
            correct_count=self._correct_count,
            rolling_accuracy=round(self._rolling_accuracy, 4),
            consecutive_correct=self._consecutive_correct,
            consecutive_wrong=self._consecutive_wrong,
            suspicious_count=self._suspicious_count,
            done=self._done,
            action_history=list(self._action_history),
            reward_history=list(self._reward_history),
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _build_observation(self) -> FraudObservation:
        """Build the observation for the current sample index."""
        sample = self._samples[self._sample_index]
        features: ExtractedFeatures = extract_features(sample)

        return FraudObservation(
            message_text=sample["message_text"],
            url=sample.get("url", ""),
            sender=sample.get("sender", "unknown"),
            extracted_features=features,
            step_count=self._step_count,
            task_name=self._task_name,
            difficulty=self._task_config["difficulty"],
            max_steps=len(self._samples),
            action_history=list(self._action_history),
            reward_history=list(self._reward_history),
        )

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def done(self) -> bool:
        return self._done
