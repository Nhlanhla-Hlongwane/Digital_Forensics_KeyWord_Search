#This is the main file for the project , its the training of the model and it calls the data_prep.py file for preprocessing
import os 
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz
import re
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
vectoriser=TfidfVectorizer()
tfidf_matrix=vectoriser.fit_transform(cleaned_docs)
print(Fore.GREEN+"Ready!\n")

# Defining the search function , it takes a query string and returns the ranked results 
# It uses cosine similarity to rank the documents based on relevance to the query
def search(query, top_n=3, score_threshold=0.01):
    all_keywords=list(set(
        kw for f in filenames
        for kw in preprocessed[f]['unique_keywords']
    ))
    # Fuzzy expand query to handlle typos and variations in the search terms
    matches=process.extract(query, all_keywords, scorer=fuzz.WRatio,limit=5)
    expanded_terms=[m[0] for m in matches if m[1]>=65]
    expanded_query=" ".join(expanded_terms) if expanded_terms else query
    
    #TF-IDF scoring
    query_vector=vectoriser.transform([expanded_query])
    scores=cosine_similarity(query_vector,tfidf_matrix).flatten()
    top_indices=scores.argsort()[::-1][:top_n]
    
    #Building the results
    results=[]
    for idx in top_indices:
        if scores[idx]>score_threshold:
            results.append({
                'rank':len(results)+1,
                'filename':filenames[idx],
                'score':round(float(scores[idx]),2),
                'preview':preprocessed[filenames[idx]]['original_text'][:200],
                'keywords_matched':expanded_terms
            })
    return results
# Highlighting the keywords in the preview text for better visualization
def highlight_keywords(text,keywords):
    for keyword in keywords:
        pattern=re.compile(re.escape(keyword),re.IGNORECASE)
        text=pattern.sub(Fore.YELLOW+Style.BRIGHT+keyword.upper()+Style.RESET_ALL+ Fore.WHITE,text)
    return text
        
#Printing the results
def print_results(query):
    results=search(query)
    print(Fore.YELLOW + f"\n{'='*60}")
    print(Fore.YELLOW + f"  Query: '{query}'")
    print(Fore.CYAN+f"  Terms: {', '.join(results[0]['keywords_matched']) if results else 'None'}")
    
    print(Fore.YELLOW + f"{'='*60}")
    if not results:
        print(Fore.RED + "  No results found.")
    
    for r in results:
        highlighted = highlight_keywords(r['preview'], r['keywords_matched'])
        print(Fore.GREEN + f"\n  #{r['rank']} {r['filename']}  (Score: {r['score']})")
        print(Fore.WHITE + f"  Preview: {highlighted}...")

    print(Fore.YELLOW + f"\n{'='*60}\n")
    
if __name__ == "__main__":
    print_results("money transfer offshore account")
    print_results("deleted files evidence")
    print_results("suspicous login password")    # typo on purpose
    print_results("drug shipment drop point")
    print_results("network traffic tor browser")