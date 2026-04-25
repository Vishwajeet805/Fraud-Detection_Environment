"""
app_ui.py — Gradio UI for Fraud Detection OpenEnv Environment.

Connects directly to existing backend classes.
Run with: python app_ui.py
"""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import random
import gradio as gr

from features import extract_features
from reward_engine import compute_reward
from models import FraudAction

# ── Constants ─────────────────────────────────────────────────────────────────

ACTION_LABELS = {0: "✅ Safe", 1: "🚨 Fraud", 2: "⚠️ Suspicious"}
ACTION_COLORS = {0: "#1a7a4a", 1: "#c0392b", 2: "#d4840a"}

FINANCIAL_FRAUD_SAVED_MIN = 5_000
FINANCIAL_FRAUD_SAVED_MAX = 20_000
FINANCIAL_FRAUD_LOST_MIN  = 10_000
FINANCIAL_FRAUD_LOST_MAX  = 50_000
FINANCIAL_AT_RISK_MIN     = 1_000
FINANCIAL_AT_RISK_MAX     = 5_000

SAFE       = 0
FRAUD      = 1
SUSPICIOUS = 2

# ── Core classifier ───────────────────────────────────────────────────────────

def classify(message: str, url: str, sender: str):
    """
    Rule-based classifier that mirrors the mock agent + reward engine logic.
    Returns (action_int, risk_score, money_saved, money_lost, money_at_risk, explanation_text)
    """
    sample = {"message_text": message, "url": url or "", "sender": sender or "unknown"}
    features = extract_features(sample)

    # ── Decision logic (mirrors mock_agent in inference.py) ──────────────────
    msg_lower    = message.lower()
    url_lower    = (url or "").lower()
    sender_lower = (sender or "").lower()

    fraud_keywords = ["otp", "pin", "aadhaar", "pan number", "won", "prize",
                      "congratulation", "blocked", "immediately", "expires",
                      "processing fee", "registration fee"]
    fraud_domains  = [".xyz", ".tk", ".ml", ".cf", ".ga", ".pw"]

    is_fraud_keyword = any(kw in msg_lower for kw in fraud_keywords)
    is_fraud_domain  = any(d in url_lower or d in sender_lower for d in fraud_domains)

    if (features.suspicious_domain_score >= 0.8 or features.sender_reputation_score >= 0.8) \
            and (features.has_urgent_words or features.has_financial_keywords):
        action = FRAUD
    elif is_fraud_keyword and (is_fraud_domain or features.suspicious_domain_score >= 0.6):
        action = FRAUD
    elif features.suspicious_domain_score >= 0.5 or features.sender_reputation_score >= 0.6:
        action = SUSPICIOUS
    elif features.has_urgent_words and features.has_financial_keywords and features.has_external_links:
        action = SUSPICIOUS
    else:
        action = SAFE

    # ── Risk score (0–100) ────────────────────────────────────────────────────
    risk_score = round(
        (features.suspicious_domain_score * 40)
        + (features.sender_reputation_score * 30)
        + (10 if features.has_urgent_words else 0)
        + (10 if features.has_financial_keywords else 0)
        + (10 if features.has_external_links else 0),
        1,
    )
    risk_score = min(risk_score, 100.0)

    # ── Financial impact ──────────────────────────────────────────────────────
    money_saved = money_lost = money_at_risk = 0.0
    if action == FRAUD:
        money_saved = float(random.randint(FINANCIAL_FRAUD_SAVED_MIN, FINANCIAL_FRAUD_SAVED_MAX))
    elif action == SAFE and features.suspicious_domain_score > 0.5:
        money_lost = float(random.randint(FINANCIAL_FRAUD_LOST_MIN, FINANCIAL_FRAUD_LOST_MAX))
    elif action == SUSPICIOUS:
        money_at_risk = float(random.randint(FINANCIAL_AT_RISK_MIN, FINANCIAL_AT_RISK_MAX))

    # ── Explanation ───────────────────────────────────────────────────────────
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

    if reasons:
        explanation_text = "This message appears risky because:\n• " + "\n• ".join(reasons)
    else:
        explanation_text = "This message appears safe with no strong fraud signals."

    return action, risk_score, money_saved, money_lost, money_at_risk, explanation_text, features


def run_analysis(message, url, sender):
    if not message.strip():
        return (
            gr.update(value="⬛ Awaiting Input", visible=True),
            gr.update(value="—"),
            gr.update(value="—"),
            gr.update(value="Please enter a message to analyse."),
            gr.update(value=""),
        )

    action, risk, saved, lost, at_risk, explanation, features = classify(message, url, sender)

    # ── Verdict card ──────────────────────────────────────────────────────────
    verdict_map = {
        FRAUD:      ("🚨 FRAUD DETECTED",      "#fff0f0", "#c0392b", "#f5c6c6"),
        SUSPICIOUS: ("⚠️ SUSPICIOUS",          "#fffbf0", "#b8860b", "#fde9a0"),
        SAFE:       ("✅ SAFE",                 "#f0fff4", "#1a7a4a", "#c3e6cb"),
    }
    label, bg, fg, border = verdict_map[action]

    verdict_html = f"""
    <div style="
        background:{bg}; border:2px solid {border}; border-radius:12px;
        padding:24px 32px; text-align:center; margin-bottom:4px;
    ">
        <div style="font-size:2rem; font-weight:800; color:{fg}; letter-spacing:1px;">
            {label}
        </div>
        <div style="margin-top:10px; font-size:1rem; color:#444;">
            Risk Score: <strong style="color:{fg}; font-size:1.3rem;">{risk:.0f} / 100</strong>
        </div>
    </div>
    """

    # ── Financial impact ──────────────────────────────────────────────────────
    if saved > 0:
        fin_html = f"""
        <div style="background:#f0fff4; border:1px solid #c3e6cb; border-radius:10px; padding:16px 20px;">
            <div style="color:#1a7a4a; font-weight:700; font-size:1rem;">💰 Money Saved</div>
            <div style="font-size:1.6rem; font-weight:800; color:#155724;">₹{saved:,.0f}</div>
            <div style="color:#555; font-size:0.85rem; margin-top:4px;">Fraud successfully blocked</div>
        </div>"""
    elif lost > 0:
        fin_html = f"""
        <div style="background:#fff0f0; border:1px solid #f5c6c6; border-radius:10px; padding:16px 20px;">
            <div style="color:#c0392b; font-weight:700; font-size:1rem;">💸 Potential Loss</div>
            <div style="font-size:1.6rem; font-weight:800; color:#721c24;">₹{lost:,.0f}</div>
            <div style="color:#555; font-size:0.85rem; margin-top:4px;">Fraud may have been missed</div>
        </div>"""
    elif at_risk > 0:
        fin_html = f"""
        <div style="background:#fffbf0; border:1px solid #fde9a0; border-radius:10px; padding:16px 20px;">
            <div style="color:#b8860b; font-weight:700; font-size:1rem;">🔍 Amount Under Review</div>
            <div style="font-size:1.6rem; font-weight:800; color:#856404;">₹{at_risk:,.0f}</div>
            <div style="color:#555; font-size:0.85rem; margin-top:4px;">Flagged for further investigation</div>
        </div>"""
    else:
        fin_html = """
        <div style="background:#f8f9fa; border:1px solid #dee2e6; border-radius:10px; padding:16px 20px;">
            <div style="color:#6c757d; font-weight:700;">💼 No Financial Impact</div>
            <div style="color:#6c757d; font-size:0.85rem; margin-top:4px;">No monetary risk detected</div>
        </div>"""

    # ── Feature badges ────────────────────────────────────────────────────────
    def badge(label, active, color):
        bg   = color if active else "#f0f0f0"
        text = "white" if active else "#aaa"
        return f'<span style="background:{bg}; color:{text}; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; margin:3px; display:inline-block;">{label}</span>'

    badges_html = f"""
    <div style="margin-top:4px;">
        {badge("🚨 Urgent Words",        features.has_urgent_words,        "#c0392b")}
        {badge("💳 Financial Keywords",  features.has_financial_keywords,  "#e67e22")}
        {badge("🌐 External Link",       features.has_external_links,      "#2980b9")}
        {badge("🕵 Suspicious Domain",   features.suspicious_domain_score > 0.6, "#8e44ad")}
        {badge("👤 Unknown Sender",      features.sender_reputation_score > 0.6, "#7f8c8d")}
    </div>
    """

    return (
        gr.update(value=verdict_html),
        gr.update(value=fin_html),
        gr.update(value=badges_html),
        gr.update(value=explanation),
        gr.update(value=""),
    )


# ── UI Layout ─────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

body, .gradio-container {
    font-family: 'DM Sans', sans-serif !important;
    background: #0f1117 !important;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.gr-box, .gr-form { background: #1a1d27 !important; border: 1px solid #2a2d3e !important; }

.header-block {
    background: linear-gradient(135deg, #1a1d27 0%, #12151f 100%);
    border: 1px solid #2a2d3e;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 8px;
}

.header-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
}

.header-sub {
    color: #8892a4;
    font-size: 0.9rem;
    margin-top: 6px;
}

label { color: #c8d0e0 !important; font-weight: 500 !important; }

textarea, input[type=text] {
    background: #12151f !important;
    border: 1px solid #2a2d3e !important;
    color: #e8eaf0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

textarea:focus, input[type=text]:focus {
    border-color: #4a6fa5 !important;
    box-shadow: 0 0 0 2px rgba(74,111,165,0.2) !important;
}

.analyze-btn {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 12px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
}

.analyze-btn:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.4) !important;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8892a4;
    margin-bottom: 8px;
}

.explain-box {
    background: #12151f !important;
    border: 1px solid #2a2d3e !important;
    border-radius: 10px !important;
    color: #c8d0e0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    padding: 14px !important;
}
"""

def build_ui():
    with gr.Blocks(css=CSS, title="Fraud Detector") as demo:

        gr.HTML("""
        <div class="header-block">
            <div class="header-title">🛡️ Fraud Detection Analyser</div>
            <div class="header-sub">
                Adaptive Phishing & Fraud Detection · OpenEnv Environment · Real-time Risk Analysis
            </div>
        </div>
        """)

        with gr.Row():
            # ── Left panel: inputs ────────────────────────────────────────────
            with gr.Column(scale=1):
                gr.HTML('<div class="section-label">Message Input</div>')

                msg_input = gr.Textbox(
                    label="Message Text",
                    placeholder="Paste the suspicious message here…",
                    lines=5,
                )
                url_input = gr.Textbox(
                    label="URL (if any)",
                    placeholder="https://example.com/link",
                    lines=1,
                )
                sender_input = gr.Textbox(
                    label="Sender",
                    placeholder="alerts@bank.com or +91-XXXXXXXXXX",
                    lines=1,
                )

                analyze_btn = gr.Button("🔍 Analyse Message", elem_classes=["analyze-btn"])

                gr.HTML('<div class="section-label" style="margin-top:20px;">Quick Test Samples</div>')
                with gr.Row():
                    ex_fraud = gr.Button("🚨 Fraud Example", size="sm")
                    ex_susp  = gr.Button("⚠️ Suspicious",    size="sm")
                    ex_safe  = gr.Button("✅ Safe Example",   size="sm")

            # ── Right panel: outputs ──────────────────────────────────────────
            with gr.Column(scale=1):
                gr.HTML('<div class="section-label">Verdict</div>')
                verdict_out = gr.HTML(
                    value='<div style="background:#1a1d27; border:1px dashed #2a2d3e; border-radius:12px; padding:32px; text-align:center; color:#4a5568;">Enter a message and click Analyse</div>'
                )

                gr.HTML('<div class="section-label" style="margin-top:16px;">Financial Impact</div>')
                finance_out = gr.HTML(
                    value='<div style="background:#1a1d27; border:1px dashed #2a2d3e; border-radius:10px; padding:20px; color:#4a5568; font-size:0.9rem;">—</div>'
                )

                gr.HTML('<div class="section-label" style="margin-top:16px;">Detected Signals</div>')
                badges_out = gr.HTML(
                    value='<div style="color:#4a5568; font-size:0.85rem;">—</div>'
                )

                gr.HTML('<div class="section-label" style="margin-top:16px;">Explanation</div>')
                explain_out = gr.Textbox(
                    label="",
                    lines=5,
                    interactive=False,
                    elem_classes=["explain-box"],
                )

                error_out = gr.HTML(visible=False)

        # ── Button wiring ─────────────────────────────────────────────────────
        outputs = [verdict_out, finance_out, badges_out, explain_out, error_out]

        analyze_btn.click(
            fn=run_analysis,
            inputs=[msg_input, url_input, sender_input],
            outputs=outputs,
        )

        # Quick example loaders
        ex_fraud.click(
            fn=lambda: (
                "URGENT: Your SBI account has been blocked! Send your OTP and PIN immediately to unblock.",
                "http://sbi-secure-verify.tk/login",
                "alert@sbi-secure-verify.tk",
            ),
            outputs=[msg_input, url_input, sender_input],
        )
        ex_susp.click(
            fn=lambda: (
                "We detected a transaction attempt on your Flipkart account from a new device. If not you, change your password.",
                "https://www.flipkart.com/account/security",
                "security@flipkart-alerts.com",
            ),
            outputs=[msg_input, url_input, sender_input],
        )
        ex_safe.click(
            fn=lambda: (
                "Your OTP for SBI Net Banking login is 482910. Valid for 5 minutes. Do not share.",
                "",
                "SBI-OTP",
            ),
            outputs=[msg_input, url_input, sender_input],
        )

    return demo


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo = build_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
    )