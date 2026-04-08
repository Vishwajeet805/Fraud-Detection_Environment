"""
tasks/hard.py — Hard task: Near-perfect phishing with subtle indicators.

15 samples designed to challenge frontier models.
Professional tone, no grammar mistakes, subtle domain differences.
"""

from __future__ import annotations
from typing import List, Dict, Any

HARD_SAMPLES: List[Dict[str, Any]] = [
    # ── FRAUD samples (label=1) — Subtle, professional-grade phishing ──────
    {
        "message_text": (
            "Dear Account Holder, we noticed a sign-in to your SBI account from a new device "
            "(Chrome on Windows, IP: 103.45.67.89). If this was you, please disregard this message. "
            "If you did not authorize this access, kindly verify your account credentials at the "
            "secure link below to prevent unauthorized transactions."
        ),
        "url": "https://sbi-secure-login.co.in/verify?token=9f3a1bc",
        "sender": "security-noreply@sbi-secure-login.co.in",
        "label": 1,
        "explanation": "Professional tone mimics SBI; domain sbi-secure-login.co.in ≠ sbi.co.in.",
    },
    {
        "message_text": (
            "We're writing to let you know that a ₹28,500 NEFT transfer has been initiated from "
            "your account. This transaction will be processed within 2 hours. If this was not "
            "authorized by you, please click the link below to raise a dispute and freeze the "
            "transaction immediately."
        ),
        "url": "https://icicibank-dispute.co.in/freeze?txn=TXN8823KL",
        "sender": "dispute@icicibank-dispute.co.in",
        "label": 1,
        "explanation": "Panic-inducing fake NEFT alert; domain icicibank-dispute.co.in ≠ icicibank.com.",
    },
    {
        "message_text": (
            "Your income tax assessment for FY 2023–24 has been completed. A refund of ₹14,320 "
            "has been approved. To credit the refund to your bank account, please confirm your "
            "account details via the Income Tax e-Filing portal link below. This must be done "
            "within 7 business days."
        ),
        "url": "https://efiling-incometax.co.in/refund-confirm",
        "sender": "refunds@efiling-incometax.co.in",
        "label": 1,
        "explanation": "Real portal is incometax.gov.in — this uses a plausible but fake .co.in domain.",
    },
    {
        "message_text": (
            "As part of our annual security audit, we are requesting all account holders to "
            "re-verify their registered mobile number and email address. Failure to verify within "
            "72 hours may result in temporary account restriction. Please use the secure portal link."
        ),
        "url": "https://axisbank-secure-portal.in/re-verify",
        "sender": "security@axisbank-secure-portal.in",
        "label": 1,
        "explanation": "axisbank-secure-portal.in ≠ axisbank.com; fake audit pretext with deadline pressure.",
    },
    {
        "message_text": (
            "Your recent application for a pre-approved personal loan of ₹5,00,000 has been reviewed. "
            "To finalize disbursement, a one-time processing charge of ₹2,500 must be paid via the "
            "link below. The loan amount will be credited within 24 hours of payment confirmation."
        ),
        "url": "https://hdfc-quickloan.in/process-fee",
        "sender": "loans@hdfc-quickloan.in",
        "label": 1,
        "explanation": "Advance fee fraud. Legitimate banks deduct fees from loan amount, not upfront.",
    },
    {
        "message_text": (
            "This is a courtesy reminder that your Aadhaar-linked mobile number will be deactivated "
            "in 48 hours due to a regulatory update. To retain your registered mobile linkage, "
            "please complete the re-verification process using the UIDAI portal below."
        ),
        "url": "https://uidai-verify-now.in/mobile-link",
        "sender": "noreply@uidai-verify-now.in",
        "label": 1,
        "explanation": "UIDAI's real domain is uidai.gov.in — uidai-verify-now.in is a spoofed civil domain.",
    },
    # ── SUSPICIOUS samples (label=2) — Ambiguous, requires deeper review ──
    {
        "message_text": (
            "We detected a transaction attempt of ₹3,200 on your Flipkart account from a new "
            "device. If this was you, no action is required. If not, please change your password "
            "from the Flipkart app or website."
        ),
        "url": "https://www.flipkart.com/account/security",
        "sender": "security@flipkart-alerts.com",
        "label": 2,
        "explanation": "URL is legitimate Flipkart, but sender domain flipkart-alerts.com ≠ flipkart.com.",
    },
    {
        "message_text": (
            "Your mutual fund SIP of ₹5,000 in HDFC Balanced Advantage Fund has been processed "
            "successfully for December. The units will be allotted within T+2 days. View your "
            "updated portfolio in the HDFC MF app."
        ),
        "url": "https://hdfcfund.com/investor",
        "sender": "portfolio@hdfcmf-statements.com",
        "label": 2,
        "explanation": "Message content normal; hdfcmf-statements.com differs from hdfcfund.com — flag for review.",
    },
    {
        "message_text": (
            "Dear customer, as part of RBI's new KYC norms effective January 1, 2025, all bank "
            "account holders are required to update their KYC documents. Please visit your nearest "
            "branch or update online via the link. Non-compliance may result in account restrictions."
        ),
        "url": "https://www.rbi.org.in/kyc-update",
        "sender": "kyc-compliance@rbi.org.in",
        "label": 2,
        "explanation": "RBI's official site is rbi.org.in — this URL matches, but rbi.org.in sender is not rbi.org.in's usual domain structure. Warrants caution.",
    },
    # ── SAFE samples (label=0) — Legitimate messages with similar structure ─
    {
        "message_text": (
            "Dear Customer, your SBI account ending 4521 has been debited ₹12,340 via NEFT to "
            "HDFC A/C 789456123. If you did not authorize this, please contact our 24x7 helpline "
            "at 1800-11-2211 or visit your nearest branch."
        ),
        "url": "",
        "sender": "alerts@sbi.co.in",
        "label": 0,
        "explanation": "Sender is @sbi.co.in (official). No link included, only helpline number.",
    },
    {
        "message_text": (
            "Your ICICI Bank credit card bill of ₹34,210 is due on December 27. To avoid late "
            "payment charges, please pay via iMobile app, internet banking, or at any ICICI branch. "
            "Thank you for banking with us."
        ),
        "url": "https://www.icicibank.com/pay",
        "sender": "creditcards@icicibank.com",
        "label": 0,
        "explanation": "Official ICICI domain. Standard billing reminder with correct bank URL.",
    },
    {
        "message_text": (
            "Reminder: Your health insurance policy #PLY-8823412 with Star Health Insurance is due "
            "for renewal on January 5, 2025. Renew now to ensure uninterrupted coverage for your "
            "family. Visit starhealth.in or call 044-28288800."
        ),
        "url": "https://www.starhealth.in/renew",
        "sender": "renewals@starhealth.in",
        "label": 0,
        "explanation": "Official Star Health domain. Standard insurance renewal reminder.",
    },
    {
        "message_text": (
            "Your DigiLocker document 'Aadhaar Card' has been successfully fetched and saved. "
            "You can access all your documents anytime at digilocker.gov.in or via the DigiLocker app."
        ),
        "url": "https://digilocker.gov.in",
        "sender": "noreply@digilocker.gov.in",
        "label": 0,
        "explanation": "Official government .gov.in domain. Routine DigiLocker notification.",
    },
    {
        "message_text": (
            "Dear Investor, your redemption request for 145.678 units of Nippon India Liquid Fund "
            "has been processed. The amount of ₹52,430.50 will be credited to your registered bank "
            "account within 1 business day."
        ),
        "url": "https://mfs.kfintech.com",
        "sender": "noreply@kfintech.com",
        "label": 0,
        "explanation": "KFin Technologies is the legitimate registrar for Nippon MF. Official domain.",
    },
    {
        "message_text": (
            "GST Filing Reminder: Your GSTR-3B for November 2024 is due on December 20, 2024. "
            "File now on the GST portal to avoid late fees. Login at gstin.gov.in."
        ),
        "url": "https://www.gstin.gov.in",
        "sender": "noreply@gstin.gov.in",
        "label": 0,
        "explanation": "Official government GST portal (.gov.in). Standard compliance reminder.",
    },
]

HARD_TASK_CONFIG = {
    "name": "hard_decision_making",
    "description": (
        "Near-perfect phishing emails with professional tone, plausible domains, and subtle differences. "
        "Includes mixed signals requiring nuanced Suspicious vs Fraud vs Safe classification."
    ),
    "difficulty": "hard",
    "passing_threshold": 0.55,
    "samples": HARD_SAMPLES,
}
