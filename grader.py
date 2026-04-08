"""
grader.py — Deterministic grader for the Fraud Detection OpenEnv environment.

Produces a score strictly between 0.01 and 0.99 (never exactly 0.0 or 1.0).
The openenv Phase 2 validator rejects exact 0.0 and exact 1.0 task scores.
No randomness. Independent of reward logic.
"""

from __future__ import annotations
from typing import List, Dict, Any
import math

from models import GraderResult

# Action constants
SAFE = 0
FRAUD = 1
SUSPICIOUS = 2

# Label weights for scoring
# False negatives (missed fraud) are penalized more than false positives.
FALSE_NEGATIVE_PENALTY = 2.0   # fraud classified as safe
FALSE_POSITIVE_PENALTY = 0.5   # safe classified as fraud
SUSPICIOUS_ON_FRAUD_CREDIT = 0.6  # at least raised a flag
SUSPICIOUS_ON_SAFE_CREDIT = 0.8   # near-miss but cautious
CORRECT_CREDIT = 1.0

# ── Score clamp: ALWAYS strictly in (0.01, 0.99) ─────────────────────────────
_SCORE_MIN = 0.01
_SCORE_MAX = 0.99


def _clamp(score: float) -> float:
    """
    Force score into strictly open interval (0.01, 0.99).
    The openenv Phase 2 validator rejects exact 0.0 and exact 1.0.
    """
    if not math.isfinite(float(score)):
        return _SCORE_MIN
    return float(max(_SCORE_MIN, min(_SCORE_MAX, score)))


def grade_single_prediction(predicted: int, label: int) -> float:
    """
    Score a single prediction against its ground-truth label.

    Returns:
        float: credit earned (0.0 to 1.0 scale, used internally only)
    and:
        is_correct (bool), is_false_negative (bool), is_false_positive (bool)
    """
    if predicted == label:
        return CORRECT_CREDIT, True, False, False

    # Fraud missed as Safe — worst outcome
    if label == FRAUD and predicted == SAFE:
        return 0.0, False, True, False

    # Fraud caught as Suspicious — partial credit
    if label == FRAUD and predicted == SUSPICIOUS:
        return SUSPICIOUS_ON_FRAUD_CREDIT, False, False, False

    # Safe labelled as Suspicious — minor error
    if label == SAFE and predicted == SUSPICIOUS:
        return SUSPICIOUS_ON_SAFE_CREDIT, False, False, False

    # Safe labelled as Fraud — false positive
    if label == SAFE and predicted == FRAUD:
        return 0.0, False, False, True

    # Suspicious labelled as Safe — acceptable
    if label == SUSPICIOUS and predicted == SAFE:
        return 0.3, False, False, False

    # Suspicious labelled as Fraud — also acceptable for borderline cases
    if label == SUSPICIOUS and predicted == FRAUD:
        return 0.5, False, False, False

    # Fallback
    return 0.0, False, False, False


def compute_episode_score(
    actions: List[int],
    labels: List[int],
    task_name: str,
) -> GraderResult:
    """
    Compute a normalized episode score from the full action/label history.

    Args:
        actions: List of agent predictions (0, 1, or 2) for each sample.
        labels:  Ground-truth labels for each sample.
        task_name: Name of the task being graded.

    Returns:
        GraderResult with score strictly in (0.01, 0.99).
    """
    if not actions or not labels:
        # FIX: return 0.01 not 0.0 — exact 0.0 fails openenv Phase 2 validator
        return GraderResult(
            task_name=task_name,
            score=_SCORE_MIN,
            correct_classifications=0,
            total_classifications=0,
            accuracy=_SCORE_MIN,
            false_negatives=0,
            false_positives=0,
            avg_reward=_SCORE_MIN,
            passed=False,
            details="No predictions provided.",
        )

    n = min(len(actions), len(labels))
    total_credit = 0.0
    max_credit = float(n) * CORRECT_CREDIT

    correct_count = 0
    false_negatives = 0
    false_positives = 0

    for i in range(n):
        credit, is_correct, is_fn, is_fp = grade_single_prediction(actions[i], labels[i])
        total_credit += credit
        if is_correct:
            correct_count += 1
        if is_fn:
            false_negatives += 1
        if is_fp:
            false_positives += 1

    raw_score = total_credit / max_credit if max_credit > 0 else 0.0

    # Penalty multiplier for missed fraud (most dangerous outcome)
    fn_penalty_factor = 1.0 - (false_negatives * 0.05)
    fn_penalty_factor = max(fn_penalty_factor, 0.5)  # floor at 50%

    raw_final = round(raw_score * fn_penalty_factor, 4)

    # FIX: clamp to strictly (0.01, 0.99) — never exactly 0.0 or 1.0
    # Previously used max(0.0, min(1.0, score)) which allowed exact 0.0 and 1.0
    score = _clamp(raw_final)

    accuracy = correct_count / n if n > 0 else 0.0

    # Passing thresholds per task
    thresholds = {
        "easy_fraud_detection": 0.75,
        "medium_risk_analysis": 0.60,
        "hard_decision_making": 0.50,
    }
    threshold = thresholds.get(task_name, 0.60)
    passed = score >= threshold

    details_parts = [
        f"Samples graded: {n}",
        f"Correct: {correct_count}/{n} ({accuracy:.1%})",
        f"False negatives (fraud missed): {false_negatives}",
        f"False positives (safe flagged): {false_positives}",
        f"Raw score: {raw_score:.4f}",
        f"FN penalty factor: {fn_penalty_factor:.4f}",
        f"Final score: {score:.4f} (clamped to 0.01–0.99)",
        f"Threshold: {threshold} | Passed: {passed}",
    ]
    details = " | ".join(details_parts)

    return GraderResult(
        task_name=task_name,
        score=score,
        correct_classifications=correct_count,
        total_classifications=n,
        accuracy=round(accuracy, 4),
        false_negatives=false_negatives,
        false_positives=false_positives,
        avg_reward=round(total_credit / n if n > 0 else _SCORE_MIN, 4),
        passed=passed,
        details=details,
    )


def run_grader(episode_history: List[Dict[str, Any]], task_config: Dict[str, Any]) -> GraderResult:
    """
    Public entry point: grade a completed episode.

    Args:
        episode_history: List of {action: int, label: int} dicts.
        task_config:     The task config dict (from tasks/*.py).

    Returns:
        GraderResult with score strictly in (0.01, 0.99).
    """
    actions = [h["action"] for h in episode_history]
    labels = [h["label"] for h in episode_history]
    return compute_episode_score(actions, labels, task_config["name"])
