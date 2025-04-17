import os
import platform
import requests
import re
import json
import datetime
import tiktoken
import random
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

MCP_SERVER_URL = 'http://localhost:9001'


mcp = FastMCP(
    "Dynamic API Tools",
    instructions="Used within MCP Custom Tool calling",
    debug=False,
    log_level="INFO",
    host="0.0.0.0",
    port=9001
)


# Get Top 10 news using news api tool
@mcp.tool()
def newsapi_get_headlines(country: str = "us") -> Any:
    """description: Get Top 10 news using news api tool using GET method for /v2/top-headlines"""
    url = "https://newsapi.org/v2/top-headlines"
    headers = {
    "Authorization": "Bearer vjdvjdj"
}
    params = {
        "country": country,
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
        return f"Request failed: {{e}}"


# The tool is used to get the satus of stocks by stock name or stock symbol, eg., APPL for Appple
@mcp.tool()
def get_stock_status(symbol: str = "IBM", interval: str = "5min", function: str = "TIME_SERIES_INTRADAY", apikey: str = "dcdcds") -> Any:
    """description: The tool is used to get the satus of stocks by stock name or stock symbol, eg., APPL for Appple using GET method for /query"""
    url = "https://www.alphavantage.co/query"
    headers = {}
    params = {
        "symbol": symbol,
        "interval": interval,
        "function": function,
        "apikey": apikey,
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
        return f"Request failed: {{e}}"


if __name__ == '__main__':
    mcp.run(transport='sse')
