from urllib.parse import urlparse
import re

TRUSTED_DOMAINS = {
    "google.com", "microsoft.com", "apple.com", "amazon.com", "paypal.com",
    "github.com", "wikipedia.org", "linkedin.com", "nytimes.com", "cnn.com"
}

TRUSTED_TLDS = {
    "com", "org", "net", "edu", "gov", "io", "co", "us", "uk", "ca", "info"
}

SUSPICIOUS_TLDS = {
    "xyz", "top", "tk", "ml", "ga", "cf", "click", "club", "buzz", "site", "online", "onion", "come"
}

TYPO_WORDS = {
    "paypa1", "goog1e", "micros0ft", "app1e", "amazo1", "faceb00k",
    "g00gle", "googie", "micr0soft", "appl3"
}

SUSPICIOUS_WORDS = {
    "darkweb", "onion", "login", "verify", "secure", "update", "account", "bank"
}

def normalize_url(url):
    url = url.strip()
    if "://" not in url:
        url = "http://" + url
    return url

def get_registrable_domain(netloc):
    parts = netloc.lower().split(".")
    if len(parts) < 2:
        return netloc.lower()
    return ".".join(parts[-2:])

def analyze_url(url):
    original = url.strip()
    if not original:
        return "Invalid Link", "Please enter a URL.", 0

    url = normalize_url(original)
    full_url = url.lower()

    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()

    if not netloc or "." not in netloc:
        return "Invalid Link", "This does not look like a valid web address.", 0

    reasons = []
    score = 0
    registrable = get_registrable_domain(netloc)

    # 1) Safe domains first
    if registrable in TRUSTED_DOMAINS:
        if any(typo in full_url for typo in TYPO_WORDS):
            return "Likely Phishing", "The website name looks misspelled and is trying to imitate a real brand.", 8
        return "Safe", "This looks like a trusted website with no obvious warning signs.", 0

    # 2) Non-trusted domains get scored
    if scheme == "http":
        score += 1
        reasons.append("This link does not use a secure connection (https).")

    if len(full_url) > 75:
        score += 1
        reasons.append("The web address is unusually long, which can be a warning sign.")

    subdomain_count = len(netloc.split(".")) - 2
    if subdomain_count >= 3:
        score += 2
        reasons.append("This link uses many extra parts in the website name, which can be used to look deceptive.")

    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", netloc):
        score += 6
        reasons.append("This link uses an IP address instead of a normal website name.")

    parts = netloc.split(".")
    tld = parts[-1]

    if tld in SUSPICIOUS_TLDS:
        score += 5
        reasons.append("The website ends with a less trusted domain extension.")
    elif tld not in TRUSTED_TLDS:
        score += 2
        reasons.append("The website uses an unusual domain extension.")

    if len(parts) >= 2:
        domain = parts[-2]
        if len(domain) <= 2:
            score += 2
            reasons.append("The website name looks unusually short or incomplete.")

        if any(typo in domain for typo in TYPO_WORDS):
            score += 8
            reasons.append("The website name looks misspelled, like it is trying to imitate a real brand.")

    if any(word in full_url for word in SUSPICIOUS_WORDS):
        score += 2
        reasons.append("The website name or path contains words often used in scam links.")

    if "%" in full_url or "@" in full_url or "!" in full_url:
        score += 1
        reasons.append("The link contains special characters that are often seen in suspicious URLs.")

    if "?" in full_url:
        score += 1
        reasons.append("The link includes extra tracking or redirect information.")

    if path.count("/") > 3:
        score += 1
        reasons.append("The address has a deep path with many sections, which can hide the real destination.")

    if not reasons:
        reasons.append("This looks like a normal website address with no obvious warning signs.")

    if score <= 2:
        label = "Safe"
    elif score <= 7:
        label = "Suspicious"
    else:
        label = "Likely Phishing"

    explanation = " ".join(reasons)
    return label, explanation, score