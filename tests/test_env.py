"""
tests/test_env.py — Full test suite for the Fraud Detection OpenEnv environment.

Run with: python -m pytest tests/ -v
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

# ── Helpers ──────────────────────────────────────────────────────────────────

def make_mock_classes():
    """Return mock Pydantic-like classes for offline testing."""
    class MockModel:
        def __init__(self, **kw):
            self.__dict__.update(kw)
        def model_dump(self):
            return self.__dict__.copy()
        def model_copy(self, update=None):
            d = self.__dict__.copy()
            if update: d.update(update)
            return type(self)(**d)

    class ExtractedFeatures(MockModel): pass
    class FraudObservation(MockModel): pass
    class FraudAction(MockModel): pass
    class FraudReward(MockModel): pass
    class StepResult(MockModel): pass
    class EnvironmentState(MockModel): pass
    class GraderResult(MockModel): pass

    return {
        'ExtractedFeatures': ExtractedFeatures,
        'FraudObservation': FraudObservation,
        'FraudAction': FraudAction,
        'FraudReward': FraudReward,
        'StepResult': StepResult,
        'EnvironmentState': EnvironmentState,
        'GraderResult': GraderResult,
    }


# ── Feature extraction tests ─────────────────────────────────────────────────

class TestFeatureExtraction:
    def setup_method(self):
        mocks = make_mock_classes()
        src = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'features.py')).read()
        src = src.replace('from models import ExtractedFeatures', '')
        self.ns = {'ExtractedFeatures': mocks['ExtractedFeatures']}
        exec(src, self.ns)

    def test_suspicious_domain_high_score(self):
        fn = self.ns['compute_suspicious_domain_score']
        score = fn('http://sbi-secure-verify.tk', 'alert@sbi-secure-verify.tk')
        assert score > 0.7

    def test_trusted_domain_zero_score(self):
        fn = self.ns['compute_suspicious_domain_score']
        score = fn('https://www.sbi.co.in', 'alerts@sbi.co.in')
        assert score == 0.0

    def test_urgent_words_detected(self):
        fn = self.ns['has_urgent_words']
        assert fn("URGENT! Your account will be suspended immediately") is True
        assert fn("Your order has been shipped") is False

    def test_financial_keywords(self):
        fn = self.ns['has_financial_keywords']
        assert fn("Send your OTP and bank account number") is True
        assert fn("See you at 3pm for the meeting") is False

    def test_extract_features_fraud_sample(self):
        fn = self.ns['extract_features']
        sample = {
            'message_text': 'URGENT: Send your OTP now! Account blocked!',
            'url': 'http://fake-bank.tk/login',
            'sender': 'alert@fake-bank.tk',
        }
        feats = fn(sample)
        assert feats.has_urgent_words is True
        assert feats.has_financial_keywords is True
        assert feats.suspicious_domain_score > 0.5

    def test_extract_features_safe_sample(self):
        fn = self.ns['extract_features']
        sample = {
            'message_text': 'Your Amazon order has been shipped.',
            'url': 'https://www.amazon.in/orders',
            'sender': 'shipment-tracking@amazon.in',
        }
        feats = fn(sample)
        assert feats.has_urgent_words is False
        assert feats.suspicious_domain_score == 0.0

    def test_domain_score_in_range(self):
        fn = self.ns['compute_suspicious_domain_score']
        for url in ['http://test.xyz', 'https://amazon.in', '', 'http://a-b-c.tk']:
            score = fn(url, '')
            assert 0.0 <= score <= 1.0, f"Score {score} out of range for {url}"


# ── Grader tests ─────────────────────────────────────────────────────────────

class TestGrader:
    def setup_method(self):
        mocks = make_mock_classes()
        src = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'grader.py')).read()
        src = src.replace('from models import GraderResult', '')
        self.ns = {'GraderResult': mocks['GraderResult']}
        exec(src, self.ns)

    def _compute(self, actions, labels, task='easy_fraud_detection'):
        return self.ns['compute_episode_score'](actions, labels, task)

    def test_perfect_score(self):
        actions = [1]*8 + [0]*7
        labels  = [1]*8 + [0]*7
        r = self._compute(actions, labels)
        assert r.score == 1.0

    def test_score_in_range(self):
        import random
        for _ in range(20):
            n = 15
            actions = [random.randint(0, 2) for _ in range(n)]
            labels  = [random.randint(0, 2) for _ in range(n)]
            r = self._compute(actions, labels)
            assert 0.0 <= r.score <= 1.0, f"Score {r.score} out of range"

    def test_all_false_negatives(self):
        actions = [0]*15
        labels  = [1]*15
        r = self._compute(actions, labels)
        assert r.false_negatives == 15
        assert r.score < 0.4

    def test_partial_credit_suspicious_on_fraud(self):
        actions = [2]*15
        labels  = [1]*15
        r = self._compute(actions, labels)
        assert 0.3 < r.score < 0.85

    def test_empty_input(self):
        r = self._compute([], [])
        assert r.score == 0.0

    def test_grader_deterministic(self):
        actions = [1, 0, 2, 1, 0, 0, 1, 2, 0, 1, 1, 0, 2, 1, 0]
        labels  = [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 2, 1, 0]
        r1 = self._compute(actions, labels)
        r2 = self._compute(actions, labels)
        assert r1.score == r2.score, "Grader must be deterministic"


# ── Reward engine tests ───────────────────────────────────────────────────────

class TestRewardEngine:
    def setup_method(self):
        mocks = make_mock_classes()
        src = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reward_engine.py')).read()
        src = src.replace('from models import FraudReward', '')
        self.ns = {'FraudReward': mocks['FraudReward']}
        exec(src, self.ns)

    def _reward(self, action, label, ah=None, rh=None):
        return self.ns['compute_reward'](action, label, ah or [], rh or [])

    def test_correct_classification(self):
        r = self._reward(1, 1)
        assert r.total == 1.0
        assert r.correct is True
        assert r.partial is False

    def test_missed_fraud_penalty(self):
        r = self._reward(0, 1)  # Fraud missed as Safe
        assert r.total == -1.5

    def test_fraud_as_suspicious_partial(self):
        r = self._reward(2, 1)
        assert r.total == 0.6
        assert r.partial is True

    def test_safe_as_suspicious_partial(self):
        r = self._reward(2, 0)
        assert r.total == 0.3
        assert r.partial is True

    def test_streak_bonus_applied(self):
        r = self._reward(1, 1, ah=[1,1,1,1], rh=[1.0,1.0,1.0,1.0])
        assert r.streak_bonus > 0

    def test_repetition_penalty(self):
        r = self._reward(0, 1, ah=[0, 0], rh=[-1.5, -1.0])
        assert r.repetition_penalty < 0

    def test_suspicious_abuse_penalty(self):
        r = self._reward(2, 1, ah=[2]*8, rh=[0.6]*8)
        assert r.suspicious_abuse_penalty < 0

    def test_reward_deterministic(self):
        r1 = self._reward(1, 1, ah=[0,1,2], rh=[1.0,-1.0,0.6])
        r2 = self._reward(1, 1, ah=[0,1,2], rh=[1.0,-1.0,0.6])
        assert r1.total == r2.total


# ── Task dataset tests ────────────────────────────────────────────────────────

class TestTaskDatasets:
    def test_easy_has_15_samples(self):
        from tasks.easy import EASY_SAMPLES
        assert len(EASY_SAMPLES) >= 15

    def test_medium_has_15_samples(self):
        from tasks.medium import MEDIUM_SAMPLES
        assert len(MEDIUM_SAMPLES) >= 15

    def test_hard_has_15_samples(self):
        from tasks.hard import HARD_SAMPLES
        assert len(HARD_SAMPLES) >= 15

    def test_all_samples_have_required_fields(self):
        from tasks import ALL_TASKS
        for task_name, cfg in ALL_TASKS.items():
            for i, s in enumerate(cfg['samples']):
                for field in ['message_text', 'url', 'sender', 'label']:
                    assert field in s, f"{task_name}[{i}] missing {field}"

    def test_all_labels_valid(self):
        from tasks import ALL_TASKS
        for task_name, cfg in ALL_TASKS.items():
            for i, s in enumerate(cfg['samples']):
                assert s['label'] in (0, 1, 2), \
                    f"{task_name}[{i}] invalid label {s['label']}"

    def test_hard_task_has_suspicious_labels(self):
        from tasks.hard import HARD_SAMPLES
        labels = {s['label'] for s in HARD_SAMPLES}
        assert 2 in labels, "Hard task should have Suspicious (2) labels"

    def test_medium_task_has_all_three_labels(self):
        from tasks.medium import MEDIUM_SAMPLES
        labels = {s['label'] for s in MEDIUM_SAMPLES}
        assert labels == {0, 1, 2}, "Medium task should have all 3 label types"


if __name__ == "__main__":
    # Run basic smoke test without pytest
    print("Running smoke tests...")
    tf = TestFeatureExtraction()
    tf.setup_method()
    tf.test_suspicious_domain_high_score()
    tf.test_trusted_domain_zero_score()
    tf.test_urgent_words_detected()
    tf.test_financial_keywords()
    tf.test_extract_features_fraud_sample()
    tf.test_extract_features_safe_sample()
    tf.test_domain_score_in_range()
    print("✓ Feature extraction tests passed")

    tg = TestGrader()
    tg.setup_method()
    tg.test_perfect_score()
    tg.test_score_in_range()
    tg.test_all_false_negatives()
    tg.test_partial_credit_suspicious_on_fraud()
    tg.test_empty_input()
    tg.test_grader_deterministic()
    print("✓ Grader tests passed")

    tr = TestRewardEngine()
    tr.setup_method()
    tr.test_correct_classification()
    tr.test_missed_fraud_penalty()
    tr.test_fraud_as_suspicious_partial()
    tr.test_safe_as_suspicious_partial()
    tr.test_streak_bonus_applied()
    tr.test_repetition_penalty()
    tr.test_suspicious_abuse_penalty()
    tr.test_reward_deterministic()
    print("✓ Reward engine tests passed")

    td = TestTaskDatasets()
    td.test_easy_has_15_samples()
    td.test_medium_has_15_samples()
    td.test_hard_has_15_samples()
    td.test_all_samples_have_required_fields()
    td.test_all_labels_valid()
    td.test_hard_task_has_suspicious_labels()
    td.test_medium_task_has_all_three_labels()
    print("✓ Task dataset tests passed")

    print("\n✅ All smoke tests passed!")
