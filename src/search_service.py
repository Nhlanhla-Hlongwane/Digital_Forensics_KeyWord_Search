import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz
from data_prep import preprocess_all

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def load_search_engine(data_dir=DATA_DIR):
    preprocessed = preprocess_all(data_dir)
    filenames = list(preprocessed.keys())
    cleaned_docs = [preprocessed[f]['cleaned_text'] for f in filenames]
    vectoriser = TfidfVectorizer()
    tfidf_matrix = vectoriser.fit_transform(cleaned_docs)
    return {
        'data_dir': data_dir,
        'preprocessed': preprocessed,
        'filenames': filenames,
        'vectoriser': vectoriser,
        'tfidf_matrix': tfidf_matrix,
    }

ENGINE = load_search_engine()


def search(query, top_n=5, score_threshold=0.01):
    if not query or not query.strip():
        return []

    all_keywords = list(set(
        kw for f in ENGINE['filenames']
        for kw in ENGINE['preprocessed'][f]['unique_keywords']
    ))

    matches = process.extract(query, all_keywords, scorer=fuzz.WRatio, limit=5)
    expanded_terms = [m[0] for m in matches if m[1] >= 65]
    expanded_query = ' '.join(expanded_terms) if expanded_terms else query

    query_vector = ENGINE['vectoriser'].transform([expanded_query])
    scores = cosine_similarity(query_vector, ENGINE['tfidf_matrix']).flatten()
    top_indices = scores.argsort()[::-1][:top_n]

    results = []
    for idx in top_indices:
        if scores[idx] > score_threshold:
            filename = ENGINE['filenames'][idx]
            results.append({
                'rank': len(results) + 1,
                'filename': filename,
                'score': round(float(scores[idx]), 2),
                'preview': ENGINE['preprocessed'][filename]['original_text'][:300],
                'keywords_matched': expanded_terms,
            })
    return results


def get_file_list():
    return [
        {
            'filename': filename,
            'unique_keywords': ENGINE['preprocessed'][filename]['unique_keywords'],
        }
        for filename in ENGINE['filenames']
    ]


def get_document(filename):
    if filename not in ENGINE['preprocessed']:
        return None
    doc = ENGINE['preprocessed'][filename]
    return {
        'filename': filename,
        'original_text': doc['original_text'],
        'cleaned_text': doc['cleaned_text'],
        'unique_keywords': doc['unique_keywords'],
    }
