"""
tasks/medium.py — Medium task: Semi-realistic phishing with mixed signals.

15 samples with borderline cases; some qualify as Suspicious (label=2).
"""

from __future__ import annotations
from typing import List, Dict, Any

MEDIUM_SAMPLES: List[Dict[str, Any]] = [
    # ── FRAUD samples (label=1) ─────────────────────────────────────────────
    {
        "message_text": "Dear valued customer, your ICICI Bank account shows unusual activity. Verify your details at the link to prevent suspension.",
        "url": "http://icici-secure-account.com/verify",
        "sender": "security@icici-secure-account.com",
        "label": 1,
        "explanation": "Mimics ICICI but domain is fake (icici-secure-account.com ≠ icicibank.com).",
    },
    {
        "message_text": "Income Tax Department: You have an unclaimed refund of ₹8,420. Submit your bank account number to receive it.",
        "url": "http://incometax-refund.in/claim",
        "sender": "refund@incometax-refund.in",
        "label": 1,
        "explanation": "IT Dept never asks for bank details via email/SMS. Fake domain.",
    },
    {
        "message_text": "Your Paytm wallet is suspended due to incomplete KYC. Click below to complete KYC within 48 hours.",
        "url": "http://paytm-kyc-verify.net/update",
        "sender": "kyc@paytm-kyc-verify.net",
        "label": 1,
        "explanation": "Paytm's real domain is paytm.com — this is a lookalike.",
    },
    {
        "message_text": "NEFT Alert: ₹45,000 debited from your account. If not done by you, click here urgently.",
        "url": "http://bankfraud-dispute.in/dispute",
        "sender": "alert@bankfraud-dispute.in",
        "label": 1,
        "explanation": "Fear-based trigger with a fraud dispute link — a phishing classic.",
    },
    {
        "message_text": "Job Offer: Amazon Hiring Work-From-Home Data Entry. Salary ₹35,000/month. Registration fee ₹500 only.",
        "url": "http://amazon-wfh-jobs.co.in/register",
        "sender": "hr@amazon-wfh-jobs.co.in",
        "label": 1,
        "explanation": "Legitimate companies never charge a registration fee for jobs.",
    },
    # ── SUSPICIOUS samples (label=2) ────────────────────────────────────────
    {
        "message_text": "Your credit card statement for November is ready. Login to view your bill and make payment.",
        "url": "http://axisbank-statements.com/login",
        "sender": "statements@axisbank-statements.com",
        "label": 2,
        "explanation": "Statement notification is expected, but domain is not axisbank.com — suspicious.",
    },
    {
        "message_text": "HDFC Bank: Transaction of ₹12,000 at Amazon India on your card ending 4521. If not you, call 1800-XXX-XXXX.",
        "url": "",
        "sender": "hdfcbank-alerts@hdfc-inform.com",
        "label": 2,
        "explanation": "Message content looks legit, but sender domain is not hdfcbank.com — warrants review.",
    },
    {
        "message_text": "Dear user, your subscription to Netflix is expiring tomorrow. Update payment to continue enjoying service.",
        "url": "https://netflix-payment-update.com/renew",
        "sender": "billing@netflix-payment-update.com",
        "label": 2,
        "explanation": "Netflix renewals come from netflix.com — this domain is suspicious.",
    },
    {
        "message_text": "Congratulations! You have been selected for a cashback of ₹250 on your last UPI transaction. Confirm your UPI ID.",
        "url": "",
        "sender": "+91-8800123456",
        "label": 2,
        "explanation": "Small cashback could be legitimate (bank promotions exist), but UPI ID request is a red flag.",
    },
    {
        "message_text": "Your Google Account had a new sign-in from Mumbai, India. If this was you, no action needed. If not, secure your account.",
        "url": "http://google-account-secure.co/review",
        "sender": "security@google-account-secure.co",
        "label": 2,
        "explanation": "Security alert content is normal but domain is not google.com.",
    },
    # ── SAFE samples (label=0) ──────────────────────────────────────────────
    {
        "message_text": "Your HDFC Bank credit card statement for November is available. Login at netbanking.hdfcbank.com to view.",
        "url": "https://netbanking.hdfcbank.com",
        "sender": "alerts@hdfcbank.com",
        "label": 0,
        "explanation": "Official HDFC domain, standard statement notification.",
    },
    {
        "message_text": "Dear Rahul, your EPF withdrawal of ₹22,000 has been processed. Amount credited within 3 working days. — EPFO",
        "url": "https://www.epfindia.gov.in",
        "sender": "noreply@epfindia.gov.in",
        "label": 0,
        "explanation": "Official government EPFO domain (.gov.in). Routine withdrawal notification.",
    },
    {
        "message_text": "Reminder: Your upcoming appointment at Apollo Hospital is scheduled for Dec 18 at 11:00 AM.",
        "url": "https://www.apollohospitals.com",
        "sender": "appointments@apollohospitals.com",
        "label": 0,
        "explanation": "Routine medical appointment reminder from official domain.",
    },
    {
        "message_text": "Your Swiggy order has been delivered. Rate your experience and get ₹20 off your next order.",
        "url": "https://www.swiggy.com/review",
        "sender": "noreply@swiggy.com",
        "label": 0,
        "explanation": "Standard post-delivery feedback from official Swiggy domain.",
    },
    {
        "message_text": "UPI payment of ₹1,500 to Reliance Jio was successful. UPI Ref: 405678901234. — PhonePe",
        "url": "",
        "sender": "noreply@phonepe.com",
        "label": 0,
        "explanation": "Official PhonePe payment confirmation. No links, no requests.",
    },
]

MEDIUM_TASK_CONFIG = {
    "name": "medium_risk_analysis",
    "description": "Classify semi-realistic phishing with mixed signals. Includes Suspicious (partial) labels.",
    "difficulty": "medium",
    "passing_threshold": 0.65,
    "samples": MEDIUM_SAMPLES,
}
