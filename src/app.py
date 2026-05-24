import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from search_service import search, get_file_list, get_document

app = FastAPI(
    title='Digital Forensics Keyword Search',
    description='Search the forensic text data from the workspace and view file details from a browser UI',
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


@app.get('/', response_class=HTMLResponse)
def index():
    html_path = os.path.join(STATIC_DIR, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as html_file:
        return html_file.read()


@app.get('/api/search')
def api_search(query: str = Query(..., min_length=1, description='Search query')):
    results = search(query)
    return {'query': query, 'results': results}


@app.get('/api/files')
def api_files():
    return {'files': get_file_list()}


@app.get('/api/file/{filename}')
def api_file(filename: str):
    document = get_document(filename)
    if document is None:
        raise HTTPException(status_code=404, detail='File not found')
    return document
