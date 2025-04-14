import requests
from typing import Any, Dict, List
from mcp import tool

@tool()
def get_https:__newsapi.org_v2_top_headlines(country: str = "default", apiKey: str = "default") -> Any:
    """
    Auto-generated GET method for https://newsapi.org/v2/top-headlines
    """
    url = "https://newsapi.org/v2/top-headlines/https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "apiKey": apiKey
    }
    try:
        response = requests.get(
            url,
            params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

