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
        # ── Multi-step scenario tracking ──────────────────────────────────
        # _current_steps: sub-steps of the active scenario
        # _current_step_index: position within those sub-steps
        # _total_steps_in_episode: sum of all sub-steps across all scenarios
        self._current_steps: List[Dict[str, Any]] = []
        self._current_step_index: int = 0
        self._total_steps_in_episode: int = 0
        self._scenario_cursor: int = -1

        # ── Multi-step helpers ────────────────────────────────────────────────

    def _get_scenario_steps(self, scenario_index: int) -> List[Dict[str, Any]]:
        """
        Return the sub-step list for a scenario.
        Backward-compatible: flat samples (no 'steps' key) return [sample].
        """
        sample = self._samples[scenario_index]
        if "steps" in sample:
            return list(sample["steps"])
        return [sample]

    def _compute_total_steps(self) -> int:
        """
        Total agent decisions across all scenarios in this task.
        Flat samples count as 1. Multi-step samples count as len(steps).
        """
        total = 0
        for s in self._samples:
            total += len(s["steps"]) if "steps" in s else 1
        return total
    def reset(self) -> FraudObservation:
        """
        Reset the environment for a new single-scenario episode.

        Each call advances to the next scenario (cycles back after the last).
        Returns the first observation of the 3-step scenario (sub-step 0).
        """
        # ── Advance scenario cursor (cycles through all scenarios) ────────
        self._scenario_cursor = (self._scenario_cursor + 1) % len(self._samples)
        self._current_steps = self._get_scenario_steps(self._scenario_cursor)
        self._current_step_index = 0

        # ── Reset all per-episode state ───────────────────────────────────
        self._step_count = 0
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

        # max_steps = steps in THIS scenario (3 for multi-step, 1 for flat)
        self._total_steps_in_episode = len(self._current_steps)

        self._current_observation = self._build_observation()
        return self._current_observation
    def step(self, action: FraudAction) -> StepResult:
        """
        Apply agent action and advance one sub-step within the current scenario.
        done=True when this scenario's 3 steps are exhausted.
        Next reset() loads the next scenario.
        """
        if self._done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")

        # ── Read current sub-step ─────────────────────────────────────────
        current_step_data = self._current_steps[self._current_step_index]
        label = current_step_data["label"]
        act = action.action

        # ── Compute reward ────────────────────────────────────────────────
        reward: FraudReward = compute_reward(
            action=act,
            label=label,
            action_history=self._action_history,
            reward_history=self._reward_history,
            step_count=self._step_count,
        )

        # ── Update history ────────────────────────────────────────────────
        self._action_history.append(act)
        self._reward_history.append(reward.total)
        self._episode_history.append({"action": act, "label": label})
        self._cumulative_reward += reward.total
        self._step_count += 1

        # ── Accuracy tracking ─────────────────────────────────────────────
        if reward.correct:
            self._correct_count += 1
            self._consecutive_correct += 1
            self._consecutive_wrong = 0
        else:
            self._consecutive_correct = 0
            self._consecutive_wrong += 1

        if act == SUSPICIOUS:
            self._suspicious_count += 1

        window = self._episode_history[-10:]
        correct_in_window = sum(1 for h in window if h["action"] == h["label"])
        self._rolling_accuracy = correct_in_window / len(window) if window else 0.0

       # ── Advance within scenario ───────────────────────────────────────
        # When a scenario's 3 steps finish, load the next scenario and
        # reset step_count so the agent sees 0→1→2 for every scenario.
        # done=True only when ALL scenarios are exhausted.
        # This keeps inference.py's single reset()+while loop working.
        self._current_step_index += 1
        scenario_exhausted = self._current_step_index >= len(self._current_steps)

        if scenario_exhausted:
            self._sample_index += 1
            if self._sample_index < len(self._samples):
                # Load next scenario, reset sub-step pointer AND step_count
                self._current_steps = self._get_scenario_steps(self._sample_index)
                self._current_step_index = 0
                self._step_count = 0   # agent sees 0,1,2 again for new scenario

        done = self._sample_index >= len(self._samples)
        self._done = done

        # ── Build next observation ────────────────────────────────────────
        if not done:
            next_obs = self._build_observation()
        else:
            next_obs = self._current_observation.model_copy(
                update={
                    "step_count": self._step_count,
                    "action_history": list(self._action_history),
                    "reward_history": list(self._reward_history),
                }
            )
        self._current_observation = next_obs

        # ── Grader fires at end of each 3-step scenario ───────────────────
        grader_result = None
        if done:
            grader_result = run_grader(self._episode_history, self._task_config)

        # Generate observation-based explanation for this step
        _features = extract_features(current_step_data)
        _obs_explanation = self._generate_explanation(current_step_data, _features)

        if _obs_explanation == ["No strong fraud signals"]:
            _explanation_text = "This message appears safe with no strong fraud signals."
        else:
            _reasons = "\n- ".join(_obs_explanation)
            _explanation_text = f"This message appears risky because:\n- {_reasons}"
        info: Dict[str, Any] = {
            "step": self._step_count,
            "label": label,
            "correct": reward.correct,
            "partial": reward.partial,
            "cumulative_reward": round(self._cumulative_reward, 4),
            "rolling_accuracy": round(self._rolling_accuracy, 4),
            "explanation": reward.explanation,
            "money_saved": reward.money_saved,
            "money_lost": reward.money_lost,
            "money_at_risk": reward.money_at_risk,
            "obs_explanation": _obs_explanation,
            "explanation_text": _explanation_text,

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
            max_steps=self._total_steps_in_episode,
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
    def _generate_explanation(self, step_data: Dict[str, Any], features) -> List[str]:
        """Generate human-readable reasons for the current observation."""
        reasons = []

        if features.has_urgent_words:
            reasons.append("Urgent language detected")
        if features.has_financial_keywords:
            reasons.append("Financial keywords present")
        if features.suspicious_domain_score > 0.6:
            reasons.append("Suspicious domain detected")
        if features.sender_reputation_score > 0.6:
            reasons.append("Low sender reputation")
        if features.has_external_links:
            reasons.append("Contains external link")

        if not reasons:
            reasons.append("No strong fraud signals")

        return reasons
    def _build_observation(self) -> FraudObservation:
        """
        Build observation from the current sub-step.
        Works for both flat samples and multi-step scenarios.
        """
        step_data = self._current_steps[self._current_step_index]
        features: ExtractedFeatures = extract_features(step_data)

        return FraudObservation(
            message_text=step_data["message_text"],
            url=step_data.get("url", ""),
            sender=step_data.get("sender", "unknown"),
            extracted_features=features,
            step_count=self._step_count,
            task_name=self._task_name,
            difficulty=self._task_config["difficulty"],
            max_steps=self._total_steps_in_episode,   # ← total sub-steps, not scenarios
            action_history=list(self._action_history),
            reward_history=list(self._reward_history),
        )
    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def done(self) -> bool:
        return self._done
