# =============================================================
# data_prep.py - Forensic Data Preprocessing Module
# Person 1 - Data & Preprocessing
# Digital Forensics Keyword Search Project
# =============================================================

import os
import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Download required NLTK data
print(Fore.CYAN + "[*] Downloading required NLTK resources...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# =============================================================
# 1. FILE LOADER
# =============================================================

def load_file(filepath):
    """Load a text file and return its contents."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(Fore.GREEN + f"[+] Loaded: {filepath}")
        return content
    except FileNotFoundError:
        print(Fore.RED + f"[-] File not found: {filepath}")
        return None

def load_all_files(data_dir):
    """Load all .txt files from the data directory."""
    files = {}
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_dir, filename)
            files[filename] = load_file(filepath)
    print(Fore.CYAN + f"\n[*] Total files loaded: {len(files)}\n")
    return files

# =============================================================
# 2. TEXT CLEANING
# =============================================================

def clean_text(text):
    """Clean and normalize raw text."""
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    # Remove IP addresses
    text = re.sub(r'\b\d{1,3}(\.\d{1,3}){3}\b', '[IP_ADDRESS]', text)
    # Remove special characters but keep spaces and alphanumerics
    text = re.sub(r'[^a-z0-9\s\[\]]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# =============================================================
# 3. TOKENIZATION
# =============================================================

def tokenize_text(text):
    """Tokenize text into words and sentences."""
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return sentences, words

# =============================================================
# 4. STOPWORD REMOVAL
# =============================================================

def remove_stopwords(words):
    """Remove common stopwords from word list."""
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in words if w not in stop_words and len(w) > 2]
    return filtered

# =============================================================
# 5. PREPROCESSING PIPELINE
# =============================================================

def preprocess(text, filename="unknown"):
    """Full preprocessing pipeline for a single document."""
    print(Fore.YELLOW + f"\n{'='*60}")
    print(Fore.YELLOW + f" Processing: {filename}")
    print(Fore.YELLOW + f"{'='*60}")

    # Original stats
    original_length = len(text)
    print(Fore.WHITE + f"  Original length   : {original_length} characters")

    # Step 1: Clean
    cleaned = clean_text(text)
    print(Fore.WHITE + f"  Cleaned length    : {len(cleaned)} characters")

    # Step 2: Tokenize
    sentences, words = tokenize_text(cleaned)
    print(Fore.WHITE + f"  Sentences found   : {len(sentences)}")
    print(Fore.WHITE + f"  Words (raw)       : {len(words)}")

    # Step 3: Remove stopwords
    filtered_words = remove_stopwords(words)
    print(Fore.WHITE + f"  Words (filtered)  : {len(filtered_words)}")

    # Step 4: Unique keywords
    unique_keywords = sorted(set(filtered_words))
    print(Fore.WHITE + f"  Unique keywords   : {len(unique_keywords)}")

    return {
        'filename'       : filename,
        'original_text'  : text,
        'cleaned_text'   : cleaned,
        'sentences'      : sentences,
        'all_words'      : words,
        'filtered_words' : filtered_words,
        'unique_keywords': unique_keywords
    }

def preprocess_all(data_dir):
    """Run preprocessing pipeline on all files."""
    print(Fore.CYAN + "\n" + "="*60)
    print(Fore.CYAN + "   FORENSIC DATA PREPROCESSING PIPELINE")
    print(Fore.CYAN + "="*60)

    files = load_all_files(data_dir)
    results = {}

    for filename, content in files.items():
        if content:
            results[filename] = preprocess(content, filename)

    # Summary table
    print(Fore.CYAN + f"\n{'='*60}")
    print(Fore.CYAN + " PREPROCESSING SUMMARY")
    print(Fore.CYAN + f"{'='*60}")

    summary = []
    for fname, res in results.items():
        summary.append({
            'File'            : fname,
            'Sentences'       : len(res['sentences']),
            'Total Words'     : len(res['all_words']),
            'Filtered Words'  : len(res['filtered_words']),
            'Unique Keywords' : len(res['unique_keywords'])
        })

    df = pd.DataFrame(summary)
    print(Fore.WHITE + df.to_string(index=False))
    print(Fore.GREEN + "\n[+] Preprocessing complete! Data is ready for NLP engine.\n")

    return results

# =============================================================
# 6. MAIN
# =============================================================

if __name__ == "__main__":
    # Path to data folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    # Run pipeline
    results = preprocess_all(data_dir)

    # Show sample keywords from each file
    print(Fore.CYAN + "="*60)
    print(Fore.CYAN + " SAMPLE KEYWORDS EXTRACTED PER FILE")
    print(Fore.CYAN + "="*60)
    for fname, res in results.items():
        print(Fore.YELLOW + f"\n  {fname}:")
        print(Fore.WHITE + f"  {res['unique_keywords'][:20]}")
