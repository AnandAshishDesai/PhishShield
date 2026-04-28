import pandas as pd
import re
from urllib.parse import urlparse
df = pd.read_csv("phishshield_90k_3categories.csv")
def extract_features(url):
    parsed = urlparse(url.lower())
    netloc = parsed.netloc
    return {
        "url_length": len(url),
        "dot_count": netloc.count("."),
        "percent_count": url.count("%"),
        "has_ip": 1 if "192.168.1.1" in netloc else 0,
        "suspicious_tld": 1 if ".tk" in netloc or ".xyz" in netloc else 0,
        "brand_typo": 1 if "paypa1" in url else 0,
        "slash_count": url.count("/"),
        "question_mark": 1 if "?" in url else 0
    }
feature_list = df["url"].apply(extract_features).tolist()
feature_df = pd.DataFrame(feature_list)
feature_df["label"] = df["label"]
feature_df.to_csv("phishshield_features.csv", index=False)
print("SUCCESS! Features extracted")
print(feature_df.head())
print(f"Shape: {feature_df.shape}")
