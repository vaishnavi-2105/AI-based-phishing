"""
utils.py — Feature extraction pipeline for Phishing URL Detection
Mirrors the exact preprocessing used during model training.
"""

import re
import math
from urllib.parse import urlparse

# ── Shortening services known to be abused by phishers ──────────────────────
SHORTENING_SERVICES = {
    "bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "t.co", "is.gd", "buff.ly",
    "adf.ly", "bit.do", "mcaf.ee", "tiny.cc", "rb.gy", "cutt.ly", "shorte.st",
    "bc.vc", "clck.ru", "url.ie", "u.to", "v.gd", "lnkd.in", "db.tt",
    "qr.ae", "po.st", "1url.com", "tweez.me", "su.pr", "twit.ac", "ff.im",
    "short.to", "tr.im", "vi.nl", "x.co"
}

# ── Keywords that commonly appear in phishing URLs ───────────────────────────
SENSITIVE_WORDS = {
    "login", "signin", "sign-in", "verify", "secure", "account", "update",
    "banking", "confirm", "password", "credential", "wallet", "paypal",
    "ebay", "amazon", "apple", "microsoft", "google", "facebook", "instagram",
    "support", "helpdesk", "refund", "suspension", "alert", "urgent",
    "billing", "invoice", "webscr", "cmd", "dispatch", "authorize"
}


def _has_ip_address(hostname: str) -> int:
    """Return 1 if the hostname is a raw IPv4 or IPv6 address."""
    ipv4 = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    ipv6 = re.compile(r"^\[?[0-9a-fA-F:]+\]?$")
    return int(bool(ipv4.match(hostname) or ipv6.match(hostname)))


def _count_subdomains(hostname: str) -> int:
    """Number of subdomains (parts before the registered domain)."""
    parts = hostname.split(".")
    # e.g. www.evil.paypal-login.com → ['www','evil','paypal-login','com']
    return max(0, len(parts) - 2)


def _is_shortened(hostname: str) -> int:
    """Return 1 if hostname matches a known URL-shortening service."""
    return int(hostname.lower() in SHORTENING_SERVICES)


def _has_sensitive_word(url: str) -> int:
    """Return 1 if the URL contains any phishing-associated keyword."""
    url_lower = url.lower()
    return int(any(word in url_lower for word in SENSITIVE_WORDS))


def _https_in_hostname(hostname: str) -> int:
    """Return 1 if 'https' literally appears inside the hostname (deceptive trick)."""
    return int("https" in hostname.lower())


def extract_features(url: str) -> list:
    """
    Extract the same 27 features used during model training.

    Feature order (must match training):
        url_length, hostname_length, path_length, query_length,
        fragment_length, num_subdomains, path_depth,
        count_dot, count_hyphen, count_underscore, count_slash,
        count_question, count_equals, count_at, count_ampersand,
        count_exclaim, count_hash, count_percent, count_plus,
        digit_count, letter_count, digit_letter_ratio,
        has_ip, has_sensitive_word, is_shortened,
        https_in_hostname, uses_https
    """
    # Ensure the URL has a scheme so urlparse works correctly
    raw = url.strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+\-.]*://", raw):
        raw = "http://" + raw

    try:
        parsed = urlparse(raw)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
        fragment = parsed.fragment or ""
    except Exception:
        hostname = path = query = fragment = ""

    # ── Lengths ──────────────────────────────────────────────────────────────
    url_length = len(url)
    hostname_length = len(hostname)
    path_length = len(path)
    query_length = len(query)
    fragment_length = len(fragment)

    # ── Structural ────────────────────────────────────────────────────────────
    num_subdomains = _count_subdomains(hostname)
    path_depth = path.count("/")

    # ── Character counts (over the full URL) ─────────────────────────────────
    count_dot = url.count(".")
    count_hyphen = url.count("-")
    count_underscore = url.count("_")
    count_slash = url.count("/")
    count_question = url.count("?")
    count_equals = url.count("=")
    count_at = url.count("@")
    count_ampersand = url.count("&")
    count_exclaim = url.count("!")
    count_hash = url.count("#")
    count_percent = url.count("%")
    count_plus = url.count("+")

    # ── Digit / letter composition ────────────────────────────────────────────
    digit_count = sum(c.isdigit() for c in url)
    letter_count = sum(c.isalpha() for c in url)
    digit_letter_ratio = (
        digit_count / letter_count if letter_count > 0 else 0.0
    )

    # ── Boolean signals ───────────────────────────────────────────────────────
    has_ip = _has_ip_address(hostname)
    has_sensitive_word = _has_sensitive_word(url)
    is_shortened = _is_shortened(hostname)
    https_in_hostname_ = _https_in_hostname(hostname)
    uses_https = int(parsed.scheme.lower() == "https")

    return [
        url_length, hostname_length, path_length, query_length,
        fragment_length, num_subdomains, path_depth,
        count_dot, count_hyphen, count_underscore, count_slash,
        count_question, count_equals, count_at, count_ampersand,
        count_exclaim, count_hash, count_percent, count_plus,
        digit_count, letter_count, digit_letter_ratio,
        has_ip, has_sensitive_word, is_shortened,
        https_in_hostname_, uses_https,
    ]


FEATURE_NAMES = [
    "url_length", "hostname_length", "path_length", "query_length",
    "fragment_length", "num_subdomains", "path_depth",
    "count_dot", "count_hyphen", "count_underscore", "count_slash",
    "count_question", "count_equals", "count_at", "count_ampersand",
    "count_exclaim", "count_hash", "count_percent", "count_plus",
    "digit_count", "letter_count", "digit_letter_ratio",
    "has_ip", "has_sensitive_word", "is_shortened",
    "https_in_hostname", "uses_https",
]
