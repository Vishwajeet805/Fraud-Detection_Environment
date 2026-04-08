"""
reward_engine.py — Sophisticated reward function for the Fraud Detection environment.

Provides dense, shaped rewards that guide learning over the full trajectory.
Not just binary end-of-episode — rewards partial progress at every step.
"""

from __future__ import annotations
from typing import List

from models import FraudReward

# ── Constants ────────────────────────────────────────────────────────────────

REWARD_CORRECT = 1.0          # Perfect classification
REWARD_PARTIAL_HIGH = 0.6     # Suspicious on Fraud (caught but not confirmed)
REWARD_PARTIAL_LOW = 0.3      # Suspicious on Safe (overcautious)
REWARD_SUSPICIOUS_ON_SUSPICIOUS = 1.0  # Correct on borderline

PENALTY_WRONG = -1.0           # Clearly wrong classification
PENALTY_MISSED_FRAUD = -1.5    # Fraud classified as Safe — most dangerous
PENALTY_REPEATED_MISTAKE = -0.2
BONUS_CORRECT_STREAK_3 = 0.1
BONUS_CORRECT_STREAK_5 = 0.2
ABUSE_SUSPICIOUS_THRESHOLD = 0.5   # >50% Suspicious usage triggers penalty
PENALTY_SUSPICIOUS_ABUSE = -0.1

SAFE = 0
FRAUD = 1
SUSPICIOUS = 2


def compute_reward(
    action: int,
    label: int,
    action_history: List[int],
    reward_history: List[float],
) -> FraudReward:
    """
    Compute shaped reward for a single step.

    Args:
        action:         Agent's action this step.
        label:          Ground-truth label for this sample.
        action_history: All previous actions (not including current).
        reward_history: All previous rewards (not including current).

    Returns:
        FraudReward with full breakdown.
    """
    base_reward = 0.0
    correct = False
    partial = False
    explanation_parts = []

    # ── Base reward ──────────────────────────────────────────────────────────
    if action == label:
        base_reward = REWARD_CORRECT
        correct = True
        explanation_parts.append(f"✓ Correct classification ({_action_name(action)}): +{REWARD_CORRECT}")

    elif label == FRAUD and action == SUSPICIOUS:
        base_reward = REWARD_PARTIAL_HIGH
        partial = True
        explanation_parts.append(f"⚠ Fraud flagged as Suspicious (partial): +{REWARD_PARTIAL_HIGH}")

    elif label == SAFE and action == SUSPICIOUS:
        base_reward = REWARD_PARTIAL_LOW
        partial = True
        explanation_parts.append(f"⚠ Safe flagged as Suspicious (overcautious): +{REWARD_PARTIAL_LOW}")

    elif label == FRAUD and action == SAFE:
        base_reward = PENALTY_MISSED_FRAUD
        explanation_parts.append(f"✗ CRITICAL: Fraud missed as Safe: {PENALTY_MISSED_FRAUD}")

    elif label == SUSPICIOUS and action == FRAUD:
        base_reward = 0.5
        partial = True
        explanation_parts.append(f"⚠ Suspicious classified as Fraud (acceptable): +0.5")

    elif label == SUSPICIOUS and action == SAFE:
        base_reward = 0.3
        partial = True
        explanation_parts.append(f"⚠ Suspicious classified as Safe (mild miss): +0.3")

    else:
        base_reward = PENALTY_WRONG
        explanation_parts.append(f"✗ Wrong classification: {PENALTY_WRONG}")

    # ── Repetition penalty ───────────────────────────────────────────────────
    repetition_penalty = 0.0
    if len(reward_history) >= 2:
        last_two_rewards = reward_history[-2:]
        if all(r < 0 for r in last_two_rewards) and base_reward < 0:
            repetition_penalty = PENALTY_REPEATED_MISTAKE
            explanation_parts.append(f"✗ Repeated mistakes penalty: {repetition_penalty}")

    # ── Streak bonus ─────────────────────────────────────────────────────────
    streak_bonus = 0.0
    if correct:
        # Count consecutive correct at tail of history
        consecutive = 0
        for prev_r in reversed(reward_history):
            if prev_r >= REWARD_CORRECT:
                consecutive += 1
            else:
                break
        if consecutive >= 4:
            streak_bonus = BONUS_CORRECT_STREAK_5
            explanation_parts.append(f"🏆 Streak bonus (5+): +{streak_bonus}")
        elif consecutive >= 2:
            streak_bonus = BONUS_CORRECT_STREAK_3
            explanation_parts.append(f"🏆 Streak bonus (3+): +{streak_bonus}")

    # ── Suspicious abuse penalty ─────────────────────────────────────────────
    suspicious_abuse_penalty = 0.0
    if action == SUSPICIOUS and len(action_history) >= 4:
        recent = action_history[-8:] + [action]
        suspicious_rate = recent.count(SUSPICIOUS) / len(recent)
        if suspicious_rate > ABUSE_SUSPICIOUS_THRESHOLD:
            suspicious_abuse_penalty = PENALTY_SUSPICIOUS_ABUSE
            explanation_parts.append(
                f"⚠ Suspicious overuse ({suspicious_rate:.0%}): {suspicious_abuse_penalty}"
            )

    total = round(
        base_reward + repetition_penalty + streak_bonus + suspicious_abuse_penalty, 4
    )

    return FraudReward(
        total=total,
        base_reward=round(base_reward, 4),
        streak_bonus=round(streak_bonus, 4),
        repetition_penalty=round(repetition_penalty, 4),
        suspicious_abuse_penalty=round(suspicious_abuse_penalty, 4),
        correct=correct,
        partial=partial,
        explanation=" | ".join(explanation_parts),
    )


def _action_name(action: int) -> str:
    return {SAFE: "Safe", FRAUD: "Fraud", SUSPICIOUS: "Suspicious"}.get(action, "Unknown")
