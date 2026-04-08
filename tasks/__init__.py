"""Tasks package for Fraud Detection OpenEnv Environment."""

from tasks.easy import EASY_TASK_CONFIG
from tasks.medium import MEDIUM_TASK_CONFIG
from tasks.hard import HARD_TASK_CONFIG

ALL_TASKS = {
    "easy_fraud_detection": EASY_TASK_CONFIG,
    "medium_risk_analysis": MEDIUM_TASK_CONFIG,
    "hard_decision_making": HARD_TASK_CONFIG,
}

__all__ = ["ALL_TASKS", "EASY_TASK_CONFIG", "MEDIUM_TASK_CONFIG", "HARD_TASK_CONFIG"]
