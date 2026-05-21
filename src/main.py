#This is the main file for the project , its the training of the model and it calls the data_prep.py file for preprocessing
import os 
import sys
from sklearn.feature_extraction.text import TfidfVectoriser
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz
from colorama import Fore, Style , init
from data_prep import preprocess_all

init(autoreset=True)

base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dat_dir=os.path.join(base_dir,'data')

print(Fore.CYAN+"Loading and preprocessing data from:", dat_dir)
preprocessed=preprocess_all(dat_dir)
filenames=list(preprocessed.keys())
cleaned_docs=[preprocessed[f]['cleaned_text'] for f in filenames]

print(Fore.CYAN+"\nVectorizing documents with TF-IDF...")
vectoriser=TfidfVectoriser()
tfidf_matrix=vectoriser.fit_transform(cleaned_docs)
print(Fore.GREEN+"Ready!\n")


