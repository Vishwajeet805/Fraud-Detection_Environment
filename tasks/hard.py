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

# ── Multi-step task: 5 scenarios × 3 sub-steps = 15 total agent decisions ──

HARD_MULTI_STEP_SAMPLES = [

    # Scenario 1: SBI account-compromise escalation (Suspicious → Fraud → Fraud)
    {
        "steps": [
            {
                "message_text": (
                    "We noticed a sign-in to your SBI account from a new device in Hyderabad. "
                    "If this was you, no action is needed. Otherwise, please review your account."
                ),
                "url": "",
                "sender": "SBI-Alerts",
                "label": 2,
                "explanation": "Plausible short-code sender; no link yet — low signal, warrants watch.",
            },
            {
                "message_text": (
                    "To secure your account following the unauthorized access attempt, please "
                    "verify your credentials via the link below within 30 minutes."
                ),
                "url": "https://sbi-secure-login.co.in/verify?session=a8f2c",
                "sender": "security@sbi-secure-login.co.in",
                "label": 1,
                "explanation": "sbi-secure-login.co.in ≠ sbi.co.in — domain impersonation confirmed.",
            },
            {
                "message_text": (
                    "An OTP has been sent to your registered mobile to complete account "
                    "verification. Enter it on the secure page to restore full account access."
                ),
                "url": "https://sbi-secure-login.co.in/otp-confirm",
                "sender": "otp@sbi-secure-login.co.in",
                "label": 1,
                "explanation": "OTP harvest on the same fake domain — final fraud step.",
            },
        ]
    },

    # Scenario 2: IT Department refund phishing chain (Suspicious → Fraud → Fraud)
    {
        "steps": [
            {
                "message_text": (
                    "Income Tax Department: A refund of ₹14,320 for FY 2023-24 is pending "
                    "processing for your PAN. Please ensure your bank details are up to date."
                ),
                "url": "",
                "sender": "+91-9845001234",
                "label": 2,
                "explanation": "Real IT Dept uses incometax.gov.in mail; phone-number sender is a soft red flag.",
            },
            {
                "message_text": (
                    "Your refund could not be auto-credited due to a bank account mismatch. "
                    "Re-submit your account details at the e-Filing portal to receive the amount."
                ),
                "url": "https://efiling-incometax.co.in/refund-resubmit",
                "sender": "refunds@efiling-incometax.co.in",
                "label": 1,
                "explanation": "efiling-incometax.co.in is not incometax.gov.in — fake portal.",
            },
            {
                "message_text": (
                    "OTP verification required to update bank account for refund credit. "
                    "Enter the OTP sent to your registered mobile on the refund portal."
                ),
                "url": "https://efiling-incometax.co.in/otp-verify",
                "sender": "noreply@efiling-incometax.co.in",
                "label": 1,
                "explanation": "OTP capture step on same fraudulent domain — completes credential theft.",
            },
        ]
    },

    # Scenario 3: Advance-fee loan fraud — clear fraud throughout (Fraud → Fraud → Fraud)
    {
        "steps": [
            {
                "message_text": (
                    "Congratulations! You have been pre-approved for an HDFC personal loan "
                    "of ₹5,00,000 at 10.5% interest. No documents required. Apply now."
                ),
                "url": "https://hdfc-quickloan.in/apply",
                "sender": "loans@hdfc-quickloan.in",
                "label": 1,
                "explanation": "hdfc-quickloan.in ≠ hdfcbank.com; unsolicited pre-approval is a scam pattern.",
            },
            {
                "message_text": (
                    "Your loan has been approved. To disburse ₹5,00,000 to your account, "
                    "a one-time processing fee of ₹2,500 is required. Pay via the link below."
                ),
                "url": "https://hdfc-quickloan.in/pay-fee",
                "sender": "disbursal@hdfc-quickloan.in",
                "label": 1,
                "explanation": "Advance fee fraud — legitimate banks never collect fees upfront via SMS.",
            },
            {
                "message_text": (
                    "Fee payment confirmed. To release the loan amount, please share the OTP "
                    "received on your mobile to authenticate the NEFT transfer."
                ),
                "url": "https://hdfc-quickloan.in/otp",
                "sender": "release@hdfc-quickloan.in",
                "label": 1,
                "explanation": "OTP steal follows advance fee payment — completes the scam.",
            },
        ]
    },

    # Scenario 4: Legitimate ICICI banking chain — all safe (Safe → Safe → Safe)
    {
        "steps": [
            {
                "message_text": (
                    "ICICI Bank: A transaction of ₹8,200 has been made on your credit card "
                    "ending 4521 at Swiggy on Dec 20. Available limit: ₹91,800."
                ),
                "url": "",
                "sender": "alerts@icicibank.com",
                "label": 0,
                "explanation": "Official icicibank.com sender, no link, routine transaction alert.",
            },
            {
                "message_text": (
                    "Your ICICI Bank credit card statement for December is ready. "
                    "Total due: ₹24,310. Minimum due: ₹1,200. Due date: January 5, 2025."
                ),
                "url": "https://www.icicibank.com/personal-banking/cards",
                "sender": "creditcards@icicibank.com",
                "label": 0,
                "explanation": "Official domain, standard billing notification with correct URL.",
            },
            {
                "message_text": (
                    "Payment of ₹24,310 received for your ICICI Bank credit card ending 4521. "
                    "Thank you. Your updated available limit is ₹1,16,110."
                ),
                "url": "https://www.icicibank.com",
                "sender": "creditcards@icicibank.com",
                "label": 0,
                "explanation": "Routine payment confirmation from official domain.",
            },
        ]
    },

    # Scenario 5: UIDAI Aadhaar phishing — starts ambiguous, escalates (Suspicious → Fraud → Fraud)
    {
        "steps": [
            {
                "message_text": (
                    "UIDAI: Your Aadhaar-linked mobile number will be deactivated in 48 hours "
                    "due to a mandatory regulatory update. Retain linkage by re-verifying."
                ),
                "url": "",
                "sender": "+91-9700112233",
                "label": 2,
                "explanation": "UIDAI communicates via uidai.gov.in, not random phone numbers — suspicious.",
            },
            {
                "message_text": (
                    "Complete your Aadhaar mobile re-verification at the UIDAI self-service portal "
                    "to prevent deactivation. The process takes under 2 minutes."
                ),
                "url": "https://uidai-selfservice.in/mobile-reverify",
                "sender": "noreply@uidai-selfservice.in",
                "label": 1,
                "explanation": "uidai-selfservice.in ≠ uidai.gov.in — fake government portal.",
            },
            {
                "message_text": (
                    "Enter your 12-digit Aadhaar number and the OTP sent to your mobile to "
                    "complete re-verification and retain your registered mobile linkage."
                ),
                "url": "https://uidai-selfservice.in/otp-verify",
                "sender": "verify@uidai-selfservice.in",
                "label": 1,
                "explanation": "Aadhaar number + OTP harvest — identity theft completion step.",
            },
        ]
    },
]

HARD_MULTI_STEP_TASK_CONFIG = {
    "name": "hard_multi_step",
    "description": (
        "Multi-step fraud scenarios: each episode contains 5 three-step chains "
        "(SMS alert → phishing link → OTP request). Agent must track signal escalation."
    ),
    "difficulty": "hard",
    "passing_threshold": 0.55,
    "samples": HARD_MULTI_STEP_SAMPLES,
}
