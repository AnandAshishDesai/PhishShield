import pandas as pd
import re
from urllib.parse import urlparse

# Load dataset
df = pd.read_csv('phishshield_90k_3categories.csv')

def extract_features(url):
    parsed = urlparse(url.lower())
    netloc = parsed.netloc
    
    return {
        'url_length': len(url),
        'dot_count': netloc.count('.'),
        'percent_count': url.count('%'),
        'has_ip': 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', netloc) else 0,
        'suspicious_tld': 1 if netloc.endswith('.xyz') or netloc.endswith('.tk') else 0,
        'brand_typo': 1 if 'paypa1' in url else 0,
        'slash_count': url.count('/'),
        'question_mark': 1 if '?' in url else 0
    }

# Extract features for all URLs
print("Extracting features from 90k URLs...")
feature_list = df['url'].apply(extract_features).tolist()
feature_df = pd.DataFrame(feature_list)
feature_df['label'] = df['label']

# Save
feature_df.to_csv('phishshield_features.csv', index=False)
print("SUCCESS! Created phishshield_features.csv")
print("\nFirst 5 rows:")
print(feature_df.head())
print(f"\nShape: {feature_df.shape}")
print("\nFeature columns:", feature_df.columns.tolist())