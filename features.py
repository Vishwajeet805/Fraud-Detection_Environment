"""
features.py — Deterministic feature extraction from raw message data.

No ML, no randomness — pure rule-based extraction for reproducibility.
"""

from __future__ import annotations
import re
from typing import Dict, Any

from models import ExtractedFeatures

# ── Keyword dictionaries ─────────────────────────────────────────────────────

URGENCY_WORDS = {
    "urgent", "immediately", "now", "expire", "expires", "expiring", "suspended",
    "suspend", "block", "blocked", "deactivate", "deactivated", "freeze", "frozen",
    "alert", "attention", "warning", "final notice", "last chance", "act now",
    "limited time", "within 24 hours", "within 48 hours", "within 72 hours",
    "asap", "hurry", "don't delay", "no delay",
}

FINANCIAL_KEYWORDS = {
    "bank", "account", "otp", "pin", "atm", "credit card", "debit card",
    "neft", "rtgs", "upi", "payment", "transfer", "transaction", "balance",
    "emi", "loan", "kyc", "aadhaar", "pan", "ifsc", "wallet", "paytm",
    "phonepe", "gpay", "refund", "withdrawal", "deposit", "salary", "income",
    "tax", "gst", "invoice", "billing", "subscription", "premium", "fee",
}

# TLDs and patterns associated with free / suspicious domains
SUSPICIOUS_TLDS = {
    ".xyz", ".tk", ".ml", ".cf", ".gq", ".ga", ".pw", ".top", ".club",
    ".info", ".biz", ".click", ".link", ".download",
}

TRUSTED_DOMAINS = {
    "sbi.co.in", "hdfcbank.com", "icicibank.com", "axisbank.com",
    "amazon.in", "amazon.com", "flipkart.com", "paytm.com", "phonepe.com",
    "goindigo.in", "irctc.co.in", "zomato.com", "swiggy.com",
    "epfindia.gov.in", "incometax.gov.in", "gstin.gov.in", "uidai.gov.in",
    "digilocker.gov.in", "rbi.org.in", "apollohospitals.com", "starhealth.in",
    "kfintech.com", "hdfcfund.com", "netbanking.hdfcbank.com",
    "bescom.co.in", "mfs.kfintech.com",
}

HOMOGRAPH_PATTERNS = [
    # Brand name in domain but not as root
    (r"sbi", r"sbi\.co\.in"),
    (r"icici", r"icicibank\.com"),
    (r"hdfc", r"hdfcbank\.com"),
    (r"axis", r"axisbank\.com"),
    (r"paytm", r"paytm\.com"),
    (r"amazon", r"amazon\.(in|com)"),
    (r"flipkart", r"flipkart\.com"),
    (r"uidai", r"uidai\.gov\.in"),
    (r"incometax", r"incometax\.gov\.in"),
    (r"rbi", r"rbi\.org\.in"),
]


def extract_domain(url: str) -> str:
    """Extract domain from a URL string."""
    url = url.strip().lower()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"/.*$", "", url)
    url = re.sub(r"\?.*$", "", url)
    return url


def compute_suspicious_domain_score(url: str, sender: str) -> float:
    """
    Returns a score between 0.0 (trusted) and 1.0 (highly suspicious).
    Deterministic — based on domain properties.
    """
    if not url and not sender:
        return 0.0

    score = 0.0
    checks = []

    url_domain = extract_domain(url) if url else ""
    sender_domain = ""
    if "@" in sender:
        sender_domain = sender.split("@")[-1].lower()

    domains_to_check = [d for d in [url_domain, sender_domain] if d]

    for domain in domains_to_check:
        # Check against trusted list
        if any(domain == td or domain.endswith("." + td) for td in TRUSTED_DOMAINS):
            checks.append(0.0)
            continue

        domain_score = 0.0

        # Suspicious TLD
        if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
            domain_score += 0.5

        # Brand name impersonation (brand in domain but not the real domain)
        for brand_pattern, real_pattern in HOMOGRAPH_PATTERNS:
            if re.search(brand_pattern, domain) and not re.search(real_pattern, domain):
                domain_score += 0.4
                break

        # Hyphenated domain (common in phishing: bank-secure-verify.com)
        hyphen_count = domain.count("-")
        if hyphen_count >= 2:
            domain_score += 0.3
        elif hyphen_count == 1:
            domain_score += 0.15

        # Long subdomain chains
        parts = domain.split(".")
        if len(parts) > 3:
            domain_score += 0.1

        checks.append(min(domain_score, 1.0))

    return round(min(max(checks) if checks else 0.0, 1.0), 3)


def has_urgent_words(text: str) -> bool:
    text_lower = text.lower()
    return any(word in text_lower for word in URGENCY_WORDS)


def has_financial_keywords(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in FINANCIAL_KEYWORDS)


def has_external_links(url: str) -> bool:
    return bool(url and url.startswith("http"))


def compute_sender_reputation(sender: str) -> float:
    """
    0.0 = highly trusted sender, 1.0 = unknown / spoofed.
    """
    if not sender or sender.startswith("+91-") or sender.isdigit():
        # Phone number — unverifiable
        return 0.5

    if "@" not in sender:
        # Short code like 'SBI-OTP' — legitimate short codes
        return 0.1

    domain = sender.split("@")[-1].lower()

    if any(domain == td or domain.endswith("." + td) for td in TRUSTED_DOMAINS):
        return 0.0

    # Check if brand name spoofed
    for brand_pattern, real_pattern in HOMOGRAPH_PATTERNS:
        if re.search(brand_pattern, domain) and not re.search(real_pattern, domain):
            return 0.85

    if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
        return 0.9

    hyphen_count = domain.count("-")
    if hyphen_count >= 2:
        return 0.7
    elif hyphen_count == 1:
        return 0.45

    return 0.3  # Unknown domain — mildly suspicious


def extract_features(sample: Dict[str, Any]) -> ExtractedFeatures:
    """Build an ExtractedFeatures object from a raw sample dict."""
    message = sample.get("message_text", "")
    url = sample.get("url", "")
    sender = sample.get("sender", "")

    return ExtractedFeatures(
        has_urgent_words=has_urgent_words(message),
        has_financial_keywords=has_financial_keywords(message),
        suspicious_domain_score=compute_suspicious_domain_score(url, sender),
        message_length=len(message),
        has_external_links=has_external_links(url),
        sender_reputation_score=compute_sender_reputation(sender),
    )
