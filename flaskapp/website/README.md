# Flask Web App Tutorial

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

## Running The App

```bash
python main.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`

SAMPLE

API: https://openlibrary.org/search.json?q=the+lord+of+the+rings
https://openlibrary.org/search.json?title=the+lord+of+the+rings
https://openlibrary.org/search.json?author=tolkien&sort=new
https://openlibrary.org/search.json?q=the+lord+of+the+rings&page=2
https://openlibrary.org/search/authors.json?q=twain
https://openlibrary.org/search.json?q=crime+and+punishment&fields=key,title,author_name,editions
https://free-apis.github.io/#/browse


url = 'https://api.waifu.im/search'
params = {
    'included_tags': ['maid'],
    'limit': '1'
}


https://api-thirukkural.vercel.app/api?num={kural_num}