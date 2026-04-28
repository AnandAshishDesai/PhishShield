import tkinter as tk
from tkinter import ttk, messagebox
from phishshield_core import analyze_url

def set_result_style(label):
    if label == "Safe":
        color = "green"
    elif label == "Suspicious":
        color = "red"
    elif label == "Likely Phishing":
        color = "orange"
    else:
        color = "black"

    result_label.config(foreground=color)
    explanation_label.config(foreground=color)
    explanation_text.config(fg=color)

def check_url():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a URL.")
        return

    label, explanation, score = analyze_url(url)

    result_label.config(text=f"Result: {label}")
    score_label.config(text=f"Risk Score: {score}")

    explanation_text.config(state="normal")
    explanation_text.delete("1.0", tk.END)
    explanation_text.insert(tk.END, explanation)
    explanation_text.config(state="disabled")

    set_result_style(label)

def clear_all():
    url_entry.delete(0, tk.END)
    result_label.config(text="Result: ", foreground="black")
    score_label.config(text="Risk Score: ", foreground="black")
    explanation_label.config(foreground="black")
    explanation_text.config(state="normal")
    explanation_text.delete("1.0", tk.END)
    explanation_text.insert(tk.END, "The explanation will appear here.")
    explanation_text.config(state="disabled")
    explanation_text.config(fg="black")

root = tk.Tk()
root.title("PhishShield - URL Checker")
root.state("zoomed")

style = ttk.Style()
style.theme_use("default")
style.configure("TButton", font=("Arial", 14), padding=10)
style.configure("TLabel", font=("Arial", 12))
style.configure("Title.TLabel", font=("Arial", 26, "bold"))

main_frame = ttk.Frame(root, padding=30)
main_frame.pack(fill="both", expand=True)

title = ttk.Label(main_frame, text="PhishShield", style="Title.TLabel")
title.pack(pady=15)

subtitle = ttk.Label(
    main_frame,
    text="Enter a URL below and click Check URL to see whether it is Safe, Suspicious, Likely Phishing, or Invalid Link."
)
subtitle.pack(pady=10)

url_entry = ttk.Entry(main_frame, width=100, font=("Arial", 14))
url_entry.pack(pady=20, fill="x")

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

check_button = ttk.Button(button_frame, text="Check URL", command=check_url)
check_button.grid(row=0, column=0, padx=15, ipadx=20, ipady=10)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_all)
clear_button.grid(row=0, column=1, padx=15, ipadx=20, ipady=10)

result_label = ttk.Label(main_frame, text="Result: ", font=("Arial", 18, "bold"))
result_label.pack(pady=20)

score_label = ttk.Label(main_frame, text="Risk Score: ", font=("Arial", 28, "bold"))
score_label.pack(pady=10)

explanation_label = ttk.Label(main_frame, text="Explanation:", font=("Arial", 14, "bold"))
explanation_label.pack(pady=(20, 5))

explanation_text = tk.Text(main_frame, height=10, wrap="word", font=("Arial", 13), fg="black")
explanation_text.pack(fill="both", expand=True)
explanation_text.insert(tk.END, "The explanation will appear here.")
explanation_text.config(state="disabled")

root.mainloop()