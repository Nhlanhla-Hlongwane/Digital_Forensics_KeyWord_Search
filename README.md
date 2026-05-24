# Digital Forensics Keyword Search

A FastAPI-powered search UI is available to query the forensic text dataset, preview documents, and inspect file keywords.

## Run the UI and API

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the FastAPI server from the `src` folder:

```bash
cd src
uvicorn app:app --reload
```

3. Open the browser:

```
http://127.0.0.1:8000
```

