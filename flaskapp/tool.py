import requests
from typing import Any, Dict, List

def get_(country: str = "country", apiKey: str = "NEWS_API_KEY") -> Any:
    """Auto-generated GET method for """
    url = "https://newsapi.org/v2/top-headlines/"
    headers = {
    "Authorization": "Basic maha:password"
}
    params = {
        "country": country,
        "apiKey": apiKey
    }
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

