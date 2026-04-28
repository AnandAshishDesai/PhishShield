import pandas as pd
import random

random.seed(42)

# Generate 30k each category
safe_urls = ['https://www.google.com/login'] * 30000
suspicious_urls = ['http://paypa1.com/verify'] * 30000
phishing_urls = ['http://192.168.1.1/update%'] * 30000

labels = (['Safe'] * 30000 +
          ['Suspicious'] * 30000 + 
          ['Likely Phishing'] * 30000)

all_urls = safe_urls + suspicious_urls + phishing_urls
combined = list(zip(all_urls, labels))
random.shuffle(combined)
urls, labels = zip(*combined)

df = pd.DataFrame({'url': urls, 'label': labels})
df.to_csv('phishshield_90k_3categories.csv', index=False)

print("SUCCESS! phishshield_90k_3categories.csv created")
print("Sample:")
print(df.head())
print(f"\nShape: {df.shape}")
print("Counts:", df['label'].value_counts().to_dict())