"""
inference.py — Baseline inference script for Fraud Detection OpenEnv.

Runs an LLM agent against all 3 tasks and prints reproducible scores.

Required environment variables:
    API_BASE_URL   The LLM API endpoint (OpenAI-compatible).
    MODEL_NAME     The model identifier.
    HF_TOKEN       Your Hugging Face / API key.

Usage:
    python inference.py

Runtime: < 20 minutes on 2 vCPU / 8 GB RAM machine.

OPENENV LOG FORMAT (mandatory — parsed by the validator):
    [START] task={task} env={env} model={model}
    [STEP]  step={n} action={action} reward={r:.4f} done={done} error={error}
    [END]   success={success} steps={n} score={score:.4f} rewards={r1,r2,...}
"""

from __future__ import annotations

import math
import os
import sys
import json
import time
import traceback
from typing import Any, Dict, List, Optional

# ── Environment setup ─────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from env import FraudDetectionEnv
from models import FraudAction
from tasks import ALL_TASKS
from grader import run_grader

# ── Configuration ─────────────────────────────────────────────────────────────

API_BASE_URL: str = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY: str = os.environ.get("HF_TOKEN") or os.environ.get("OPENAI_API_KEY") or ""
MODEL_NAME: str = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

MAX_RETRIES: int = 3
RETRY_DELAY: float = 2.0
TEMPERATURE: float = 0.1
MAX_TOKENS: int = 150

ENV_NAME = "fraud-detection-env"

# ── Score clamp ───────────────────────────────────────────────────────────────

def _clamp(v: float) -> float:
    """Always return a float strictly in (0.01, 0.99)."""
    if not math.isfinite(float(v)):
        return 0.01
    return max(0.01, min(0.99, float(v)))

# ── MANDATORY OPENENV LOG FORMAT ──────────────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    # Use 4dp to prevent rounding to 0.00 or 1.00
    safe_reward = _clamp(reward) if reward >= 0 else reward  # keep negative rewards as-is (shaped rewards)
    error_val = error if error else "null"
    done_val  = str(done).lower()
    print(
        f"[STEP] step={step} action={action} "
        f"reward={safe_reward:.4f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    """
    Emit [END] line with score= field that the openenv validator reads.
    score is clamped to strictly (0.01, 0.99).
    rewards list uses the same 4dp format.
    """
    safe_score = _clamp(score)
    # For rewards list, clamp to (0.01, 0.99) — the validator may check these too
    safe_rewards = [_clamp(r) for r in rewards] if rewards else [0.01]
    rewards_str = ",".join(f"{r:.4f}" for r in safe_rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={safe_score:.4f} rewards={rewards_str}",
        flush=True,
    )

# ── Prompts ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a cybersecurity analyst specializing in fraud and phishing detection.

You will be shown a message or transaction. Classify it as exactly one of:
  0 = Safe      (legitimate message, no fraud indicators)
  1 = Fraud     (definitely fraudulent / phishing)
  2 = Suspicious (mixed signals, requires further review)

Key indicators to check:
- Domain spoofing (e.g. sbi-secure-login.co.in ≠ sbi.co.in)
- Urgency language (URGENT, IMMEDIATELY, EXPIRES)
- Requests for sensitive data (PIN, OTP, Aadhaar, PAN)
- Registration/processing fees for loans or jobs
- Financial threats (account blocked, legal action)
- Sender domain mismatch with claimed organization

Respond with ONLY a JSON object in this exact format:
{"action": <0, 1, or 2>, "reasoning": "<brief reason>"}

No other text. No markdown. Just valid JSON."""


def build_user_prompt(obs: Dict[str, Any]) -> str:
    features = obs.get("extracted_features", {})
    lines = [
        f"Message: {obs.get('message_text', '')}",
        f"URL: {obs.get('url', '(none)')}",
        f"Sender: {obs.get('sender', 'unknown')}",
        "",
        "Extracted Features:",
        f"  - Urgent words detected: {features.get('has_urgent_words', False)}",
        f"  - Financial keywords: {features.get('has_financial_keywords', False)}",
        f"  - Suspicious domain score: {features.get('suspicious_domain_score', 0.0):.2f} (0=trusted, 1=suspicious)",
        f"  - Sender reputation score: {features.get('sender_reputation_score', 0.0):.2f} (0=trusted, 1=unknown)",
        f"  - Has external links: {features.get('has_external_links', False)}",
        "",
        "Classify as 0=Safe, 1=Fraud, 2=Suspicious.",
        'Respond with only: {"action": <0/1/2>, "reasoning": "<brief reason>"}',
    ]
    return "\n".join(lines)


# ── LLM client (optional — falls back to mock agent if unavailable) ───────────

_client = None

def _init_client():
    global _client
    if not API_KEY:
        print("[INFO] No API key found — using mock agent (rule-based fallback).", flush=True)
        return
    try:
        from openai import OpenAI
        _client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
        print(f"[INFO] OpenAI client ready — model: {MODEL_NAME}", flush=True)
    except ImportError:
        print("[WARN] openai package not installed — using mock agent.", flush=True)
    except Exception as exc:
        print(f"[WARN] Failed to create OpenAI client: {exc} — using mock agent.", flush=True)


def mock_agent(obs: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based fallback agent used when LLM is unavailable."""
    features = obs.get("extracted_features", {})
    msg = obs.get("message_text", "").lower()
    url = obs.get("url", "").lower()
    sender = obs.get("sender", "").lower()

    suspicious_domain = features.get("suspicious_domain_score", 0.0)
    sender_rep = features.get("sender_reputation_score", 0.0)
    has_urgent = features.get("has_urgent_words", False)
    has_financial = features.get("has_financial_keywords", False)
    has_links = features.get("has_external_links", False)

    # Strong fraud signals
    fraud_keywords = ["otp", "pin", "aadhaar", "pan number", "won", "prize",
                      "congratulation", "blocked", "immediately", "expires"]
    fraud_domains = [".xyz", ".tk", ".ml", ".cf", ".ga", ".pw"]

    is_fraud_keyword = any(kw in msg for kw in fraud_keywords)
    is_fraud_domain = any(d in url or d in sender for d in fraud_domains)

    if (suspicious_domain >= 0.8 or sender_rep >= 0.8) and (has_urgent or has_financial):
        return {"action": 1, "reasoning": "High suspicion domain/sender with urgency/financial keywords — fraud"}

    if is_fraud_keyword and (is_fraud_domain or suspicious_domain >= 0.6):
        return {"action": 1, "reasoning": "Fraud keywords + suspicious domain"}

    if suspicious_domain >= 0.5 or sender_rep >= 0.6:
        return {"action": 2, "reasoning": "Moderate domain/sender risk — suspicious"}

    if has_urgent and has_financial and has_links:
        return {"action": 2, "reasoning": "Urgency + financial + links — suspicious"}

    return {"action": 0, "reasoning": "No strong fraud signals detected — safe"}


def call_llm(obs: Dict[str, Any]) -> Dict[str, Any]:
    """Call LLM or fall back to mock agent. Never raises."""
    if _client is None:
        return mock_agent(obs)

    prompt = build_user_prompt(obs)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = _client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            content = (response.choices[0].message.content or "{}").strip()
            if content.startswith("```"):
                content = "\n".join(
                    l for l in content.split("\n") if not l.startswith("```")
                ).strip()
            parsed = json.loads(content)
            action = int(parsed.get("action", 2))
            if action not in (0, 1, 2):
                action = 2
            return {"action": action, "reasoning": parsed.get("reasoning", "")}
        except json.JSONDecodeError:
            import re
            m = re.search(r'"action"\s*:\s*([012])', content)
            if m:
                return {"action": int(m.group(1)), "reasoning": "parsed from malformed JSON"}
            if attempt == MAX_RETRIES:
                return {"action": 2, "reasoning": f"JSON parse failed: {content[:80]}"}
        except Exception as exc:
            if attempt == MAX_RETRIES:
                return {"action": 2, "reasoning": f"API error: {str(exc)[:60]}"}
            time.sleep(RETRY_DELAY * attempt)

    return {"action": 2, "reasoning": "fallback after retries"}


ACTION_NAMES = {0: "Safe", 1: "Fraud", 2: "Suspicious"}


# ── Episode runner ────────────────────────────────────────────────────────────

def run_task(task_name: str) -> Dict[str, Any]:
    """Run one full episode on a task. Always returns a result dict."""
    agent_name = MODEL_NAME if _client else "mock_agent"

    # Emit mandatory [START] line in exact openenv format
    log_start(task=task_name, env=ENV_NAME, model=agent_name)

    step_rewards: List[float] = []
    episode_history: List[Dict[str, Any]] = []
    steps_taken = 0
    score = 0.01

    try:
        env = FraudDetectionEnv(task_name=task_name)
        obs = env.reset().model_dump()

        while not env.done:
            steps_taken += 1
            llm_result = call_llm(obs)
            action_int = llm_result["action"]
            reasoning  = llm_result.get("reasoning", "")

            action = FraudAction(action=action_int, reasoning=reasoning)

            error_msg = None
            done = False
            reward_val = 0.01
            try:
                result     = env.step(action)
                reward_val = result.reward.total   # shaped reward (can be negative)
                done       = result.done

                episode_history.append({
                    "action": action_int,
                    "label":  result.info.get("label", -1),
                })
                step_rewards.append(reward_val)
                obs = result.observation.model_dump()

            except Exception as exc:
                error_msg = str(exc)[:60]
                done = True

            # Emit mandatory [STEP] line
            log_step(
                step=steps_taken,
                action=ACTION_NAMES.get(action_int, str(action_int)),
                reward=reward_val,
                done=done,
                error=error_msg,
            )

            if done:
                break

        # Grade the episode
        task_config = ALL_TASKS[task_name]
        grader_result = run_grader(episode_history, task_config)
        score = grader_result.score  # already clamped to (0.01, 0.99) by grader

    except Exception as exc:
        print(f"[ERROR] Task '{task_name}' failed: {exc}", flush=True)
        traceback.print_exc()
        score = 0.01

    # Emit mandatory [END] line with score= field
    log_end(
        success=score >= 0.5,
        steps=steps_taken,
        score=score,
        rewards=step_rewards,
    )

    return {
        "task_name": task_name,
        "score":     score,
        "steps":     steps_taken,
        "passed":    score >= ALL_TASKS[task_name].get("passing_threshold", 0.6),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # Global safety net — inference.py must NEVER exit with an unhandled exception.
    # The openenv validator treats non-zero exit as failure.
    try:
        _main_inner()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[ERROR] Unexpected top-level error: {exc}", flush=True)
        traceback.print_exc()
        # Emit fallback [END] for every task so the validator gets valid scores
        for task_name in ALL_TASKS:
            log_start(task=task_name, env=ENV_NAME, model="mock_agent")
            log_end(success=False, steps=0, score=0.01, rewards=[])
        sys.exit(0)


def _main_inner() -> None:
    print("=" * 60, flush=True)
    print("Fraud Detection OpenEnv — Baseline Inference", flush=True)
    print("=" * 60, flush=True)
    print(f"API Base URL : {API_BASE_URL}", flush=True)
    print(f"Model        : {MODEL_NAME}", flush=True)
    print(f"Tasks        : {list(ALL_TASKS.keys())}", flush=True)
    print("=" * 60, flush=True)

    # FIX: no sys.exit on missing API key — fall back to mock agent gracefully
    _init_client()

    all_results = []
    for task_name in ALL_TASKS:
        try:
            result = run_task(task_name)
            all_results.append(result)
        except Exception as exc:
            print(f"\n[ERROR] Task '{task_name}' raised unexpectedly:", flush=True)
            traceback.print_exc()
            # Emit fallback [END] — validator must always get a score line
            log_start(task=task_name, env=ENV_NAME, model="mock_agent")
            log_end(success=False, steps=0, score=0.01, rewards=[])
            all_results.append({"task_name": task_name, "score": 0.01, "passed": False})

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 60, flush=True)
    print("FINAL SUMMARY", flush=True)
    print("=" * 60, flush=True)
    print(f"{'Task':<30} {'Score':>7} {'Passed':>7}", flush=True)
    print("-" * 50, flush=True)

    total_score = 0.0
    for r in all_results:
        s = _clamp(r.get("score", 0.01))
        total_score += s
        passed_str = "✓" if r.get("passed") else "✗"
        print(f"{r['task_name']:<30} {s:>7.4f} {passed_str:>7}", flush=True)

    avg = _clamp(total_score / len(all_results)) if all_results else 0.01
    print("-" * 50, flush=True)
    print(f"{'AVERAGE':<30} {avg:>7.4f}", flush=True)
    print("=" * 60, flush=True)

    summary = {
        "model":         MODEL_NAME if _client else "mock_agent",
        "tasks":         all_results,
        "average_score": round(avg, 4),
    }
    print("\n[JSON_SUMMARY]", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
