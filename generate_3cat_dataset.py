import pandas as pd
import random
from urllib.parse import urlunparse

random.seed(42)

safe_brands = [
    "google", "apple", "microsoft", "amazon", "paypal",
    "wikipedia", "github", "linkedin", "cnn", "nytimes"
]

safe_tlds = ["com", "org", "edu", "gov", "net"]
suspicious_tlds = ["xyz", "top", "tk", "ml", "info", "club", "click"]
suspicious_words = ["login", "secure", "verify", "update", "account", "support", "billing"]
path_words = ["home", "login", "account", "portal", "dashboard", "review", "help", "status"]
phish_paths = ["login", "verify", "reset-password", "secure-check", "confirm", "update-payment"]

def random_domain(base_words, tlds):
    name = random.choice(base_words)
    suffix = random.choice(tlds)
    return f"www.{name}.{suffix}"

def typo_brand():
    brand = random.choice(safe_brands)
    typo_choices = [
        brand[:-1] + "1",
        brand[:-1] + "0",
        brand.replace("o", "0"),
        brand.replace("l", "1"),
        brand + random.choice(["-secure", "-login", "-verify"])
    ]
    return random.choice(typo_choices)

def generate_safe_url():
    scheme = random.choice(["https", "https", "http"])
    domain = random_domain(safe_brands, safe_tlds)
    path = "/" + "/".join(random.choices(path_words, k=random.randint(0, 2)))
    if path == "/":
        path = "/home"
    return urlunparse((scheme, domain, path, "", "", ""))

def generate_suspicious_url():
    scheme = random.choice(["http", "https"])
    if random.random() < 0.5:
        domain = f"{random.choice(suspicious_words)}.{typo_brand()}.{random.choice(safe_tlds)}"
    else:
        sub1 = random.choice(["secure", "login", "update", "verify"])
        sub2 = random.choice(["account", "user", "payment", "portal"])
        domain = f"{sub1}.{sub2}.{typo_brand()}.{random.choice(safe_tlds)}"
    path = "/" + "/".join(random.choices(["login", "verify", "update", "confirm"], k=random.randint(1, 2)))
    if random.random() < 0.5:
        path += f"?id={random.randint(1000,99999)}"
    return urlunparse((scheme, domain, path, "", "", ""))

def generate_likely_phishing_url():
    scheme = random.choice(["http", "https"])
    if random.random() < 0.4:
        domain = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    else:
        subs = ".".join(random.choices(["secure", "login", "update", "verify", "account", "bank"], k=random.randint(3, 6)))
        domain = f"{subs}.{typo_brand()}.{random.choice(suspicious_tlds)}"
    path = "/" + "/".join(random.choices(phish_paths, k=random.randint(2, 5)))
    if random.random() < 0.7:
        path += f"?redirect={random.choice(safe_brands)}.com&token={random.randint(1000,999999)}"
    if random.random() < 0.5:
        path += random.choice(["%", "@", "!", "*"])
    return urlunparse((scheme, domain, path, "", "", ""))

def make_dataset(n=30000):
    safe = [generate_safe_url() for _ in range(n)]
    suspicious = [generate_suspicious_url() for _ in range(n)]
    phishing = [generate_likely_phishing_url() for _ in range(n)]
    labels = (["Safe"] * n) + (["Suspicious"] * n) + (["Likely Phishing"] * n)
    urls = safe + suspicious + phishing
    rows = list(zip(urls, labels))
    random.shuffle(rows)
    return pd.DataFrame(rows, columns=["url", "label"])

df = make_dataset(30000)
df.to_csv("phishshield_90k_3categories.csv", index=False)

print("SUCCESS: phishshield_90k_3categories.csv")
print("Shape:", df.shape)
print(df["label"].value_counts().to_dict())
print(df.head(10))