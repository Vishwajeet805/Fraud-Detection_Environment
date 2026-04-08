"""
models.py — Typed Pydantic models for the Fraud Detection OpenEnv Environment.

Defines Observation, Action, and Reward models per OpenEnv specification.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------

class ExtractedFeatures(BaseModel):
    """Structured features extracted from the input message / transaction."""

    has_urgent_words: bool = Field(
        description="True if the message contains urgency-inducing language."
    )
    has_financial_keywords: bool = Field(
        description="True if financial keywords (OTP, account, payment, etc.) appear."
    )
    suspicious_domain_score: float = Field(
        ge=0.0, le=1.0,
        description="0 = trusted domain, 1 = highly suspicious domain / URL."
    )
    message_length: int = Field(
        ge=0,
        description="Character count of the raw message text."
    )
    has_external_links: bool = Field(
        description="True if the message contains HTTP/HTTPS links."
    )
    sender_reputation_score: float = Field(
        ge=0.0, le=1.0,
        description="0 = known trusted sender, 1 = unknown / spoofed sender."
    )


class FraudObservation(BaseModel):
    """
    Full observation returned to the agent at each step.
    Contains raw input plus pre-computed features.
    """

    # Raw inputs
    message_text: str = Field(description="The raw message or transaction description.")
    url: str = Field(description="URL contained in the message (empty string if none).")
    sender: str = Field(description="Sender identifier (email, phone, or 'unknown').")

    # Pre-computed features to help the agent
    extracted_features: ExtractedFeatures

    # Episode metadata
    step_count: int = Field(ge=0, description="Current step index (0-based).")
    task_name: str = Field(description="Active task identifier.")
    difficulty: str = Field(description="Current difficulty: easy | medium | hard.")
    max_steps: int = Field(description="Maximum steps allowed in this episode.")

    # Context window
    action_history: List[int] = Field(
        default_factory=list,
        description="List of agent actions taken so far (0=Safe, 1=Fraud, 2=Suspicious)."
    )
    reward_history: List[float] = Field(
        default_factory=list,
        description="Rewards received for each previous step."
    )


# ---------------------------------------------------------------------------
# Action
# ---------------------------------------------------------------------------

class FraudAction(BaseModel):
    """
    Agent's classification decision.

    0 = Safe       — message is legitimate
    1 = Fraud      — message is definitely fraudulent
    2 = Suspicious — message needs further scrutiny
    """

    action: int = Field(
        ge=0, le=2,
        description="Classification: 0=Safe, 1=Fraud, 2=Suspicious."
    )
    confidence: Optional[float] = Field(
        default=None, ge=0.0, le=1.0,
        description="Optional confidence score from the agent (0–1)."
    )
    reasoning: Optional[str] = Field(
        default=None,
        description="Optional textual reasoning from the agent."
    )


# ---------------------------------------------------------------------------
# Reward
# ---------------------------------------------------------------------------

class FraudReward(BaseModel):
    """Detailed reward breakdown for transparency and debugging."""

    total: float = Field(description="Net reward for this step.")
    base_reward: float = Field(description="Core correctness reward.")
    streak_bonus: float = Field(default=0.0, description="Bonus for correct streaks.")
    repetition_penalty: float = Field(default=0.0, description="Penalty for repeated errors.")
    suspicious_abuse_penalty: float = Field(
        default=0.0, description="Penalty for over-using 'Suspicious' label."
    )
    correct: bool = Field(description="Whether the action was the optimal choice.")
    partial: bool = Field(description="Whether partial credit was awarded.")
    explanation: str = Field(description="Human-readable reward explanation.")


# ---------------------------------------------------------------------------
# Step result & State
# ---------------------------------------------------------------------------

class StepResult(BaseModel):
    """Full result returned by env.step()."""

    observation: FraudObservation
    reward: FraudReward
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)


class EnvironmentState(BaseModel):
    """Complete environment state snapshot from env.state()."""

    task_name: str
    difficulty: str
    step_count: int
    max_steps: int
    current_sample_index: int
    total_samples: int
    cumulative_reward: float
    correct_count: int
    rolling_accuracy: float
    consecutive_correct: int
    consecutive_wrong: int
    suspicious_count: int
    done: bool
    action_history: List[int]
    reward_history: List[float]


# ---------------------------------------------------------------------------
# Task / Grader result
# ---------------------------------------------------------------------------

class GraderResult(BaseModel):
    """Result from the programmatic grader for a completed episode."""

    task_name: str
    score: float = Field(ge=0.01, le=0.99, description="Final normalized score strictly in (0.01, 0.99).")
    correct_classifications: int
    total_classifications: int
    accuracy: float
    false_negatives: int = Field(description="Fraud missed as Safe — most critical.")
    false_positives: int = Field(description="Safe messages flagged as Fraud.")
    avg_reward: float
    passed: bool
    details: str
