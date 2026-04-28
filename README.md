# PhishShield

PhishShield is a Python-based phishing URL checker with a desktop GUI. It analyzes a URL, classifies it as **Safe**, **Suspicious**, or **Likely Phishing**, and explains the result in simple language for non-technical users.

## Features
- Desktop GUI built with Tkinter
- URL classification into 3 categories
- Human-friendly explanation for each result
- Clear button to reset the form
- Full-screen style window for easy use

## How It Works
PhishShield checks common phishing signals such as:
- suspicious or misspelled domain names
- unusual top-level domains
- IP addresses in URLs
- long or complex web addresses
- special characters and redirect patterns

## Files
- `phishshield_core.py` — main URL checking logic
- `phishshield_gui.py` — desktop interface
- `phishshield.py` — older script version
- `generate_3cat_dataset.py` — synthetic dataset generator
- `phishshield_90k_3categories.csv` — generated dataset
- `extract_features.py` — feature extraction script
- `features.py` — feature definitions
- `phishshield_scored.csv` — scored output
- `phishshield_final_results.csv` — final labeled output

## How to Run
1. Open the project in VS Code.
2. Make sure your Python environment is active.
3. Run:

```bash
python phishshield_gui.py
```

Or use your project environment directly:

```bash
"/Users/anand/python programs/PhishShield/env/bin/python" "/Users/anand/python programs/PhishShield/phishshield_gui.py"
```

## Example
- `google.com` → Safe
- `paypa1.com` → Likely Phishing
- `http://192.168.1.1/login` → Likely Phishing

## Notes
This project uses rule-based detection and a synthetic dataset for demonstration and learning purposes.
