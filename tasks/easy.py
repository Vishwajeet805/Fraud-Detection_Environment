"""
tasks/easy.py — Easy task: Obvious fraud with clear signals.

15 samples with unambiguous fraud / safe labels.
"""

from __future__ import annotations
from typing import List, Dict, Any

EASY_SAMPLES: List[Dict[str, Any]] = [
    # ── FRAUD samples (label=1) ─────────────────────────────────────────────
    {
        "message_text": "CONGRATULATIONS!!! You have WON ₹50,000!!! Click NOW to claim your prize before it EXPIRES!!!",
        "url": "http://win-prize-now.xyz/claim",
        "sender": "prize@lottery-free.xyz",
        "label": 1,
        "explanation": "All-caps urgency, fake lottery, suspicious .xyz domain.",
    },
    {
        "message_text": "Your bank account is BLOCKED. Send your ATM PIN and OTP immediately to unblock.",
        "url": "http://sbi-secure-verify.tk/login",
        "sender": "alert@sbi-secure-verify.tk",
        "label": 1,
        "explanation": "Asks for PIN/OTP — banks never do this. Fake domain.",
    },
    {
        "message_text": "FREE iPhone 15 Pro! You are our 1,000,000th visitor. Enter credit card to pay ₹1 shipping.",
        "url": "http://free-iphone-india.ml/claim",
        "sender": "noreply@free-iphone-india.ml",
        "label": 1,
        "explanation": "Classic too-good-to-be-true bait with CC harvesting.",
    },
    {
        "message_text": "URGENT: Transfer ₹1 Lakh in 2 hours or your account gets permanently suspended.",
        "url": "http://rbi-alert.cf/suspend",
        "sender": "rbi.alert@rbi-india.cf",
        "label": 1,
        "explanation": "Extreme urgency + fake RBI domain + financial threat.",
    },
    {
        "message_text": "You have unpaid EMI. Pay ₹500 NOW or we will file police case against you.",
        "url": "http://loanrecover-india.tk/pay",
        "sender": "legal@loanrecover-india.tk",
        "label": 1,
        "explanation": "Threatening language, fake legal action, suspicious TLD.",
    },
    {
        "message_text": "Dear customer send your Aadhaar number, PAN, and bank details to avail government subsidy.",
        "url": "",
        "sender": "+91-9999999999",
        "label": 1,
        "explanation": "Requests multiple sensitive documents. Government never asks via SMS.",
    },
    {
        "message_text": "KYC UPDATE REQUIRED IMMEDIATELY or your account will be deactivated within 24 hours!!!",
        "url": "http://hdfc-kyc-update.gq/kyc",
        "sender": "kyc@hdfc-kyc-update.gq",
        "label": 1,
        "explanation": "Fake KYC urgency with .gq free domain spoofing HDFC.",
    },
    {
        "message_text": "Earn ₹5000/day working from home. No experience needed. WhatsApp NOW: 9876543210",
        "url": "",
        "sender": "+91-9876543210",
        "label": 1,
        "explanation": "Work-from-home scam with unrealistic earnings promise.",
    },
    # ── SAFE samples (label=0) ──────────────────────────────────────────────
    {
        "message_text": "Your OTP for SBI Net Banking login is 482910. Valid for 5 minutes. Do not share.",
        "url": "",
        "sender": "SBI-OTP",
        "label": 0,
        "explanation": "Legitimate OTP from official sender short code. No link, no request.",
    },
    {
        "message_text": "Your Amazon order #405-1234567-8901234 has been shipped. Delivery expected by Dec 12.",
        "url": "https://www.amazon.in/orders",
        "sender": "shipment-tracking@amazon.in",
        "label": 0,
        "explanation": "Official Amazon tracking notification. Trusted domain.",
    },
    {
        "message_text": "Reminder: Your electricity bill of ₹1,240 is due on 25th December. Pay at bescom.co.in",
        "url": "https://bescom.co.in/pay",
        "sender": "noreply@bescom.co.in",
        "label": 0,
        "explanation": "Routine utility bill reminder from official domain.",
    },
    {
        "message_text": "Your flight IndiGo 6E-201 on Dec 20 is confirmed. Check-in opens 48 hours before departure.",
        "url": "https://www.goindigo.in/checkin",
        "sender": "noreply@goindigo.in",
        "label": 0,
        "explanation": "Official airline booking confirmation.",
    },
    {
        "message_text": "Hi, I'd like to schedule a meeting for next Monday at 3 PM. Please confirm availability.",
        "url": "",
        "sender": "manager@company.com",
        "label": 0,
        "explanation": "Normal professional email with no suspicious signals.",
    },
    {
        "message_text": "Your IRCTC ticket PNR 4561237890 is booked. Train 12345 on Dec 15. Seat: S2/34.",
        "url": "https://www.irctc.co.in/nget/train-search",
        "sender": "no_reply@irctc.co.in",
        "label": 0,
        "explanation": "Official IRCTC booking confirmation.",
    },
    {
        "message_text": "Your Zomato order from Burger King is on its way! Track your order in the app.",
        "url": "https://www.zomato.com/orders",
        "sender": "noreply@zomato.com",
        "label": 0,
        "explanation": "Legitimate food delivery notification from official domain.",
    },
]

EASY_TASK_CONFIG = {
    "name": "easy_fraud_detection",
    "description": "Detect obvious fraud: scam messages with clear red flags vs. legitimate notifications.",
    "difficulty": "easy",
    "passing_threshold": 0.75,
    "samples": EASY_SAMPLES,
}
