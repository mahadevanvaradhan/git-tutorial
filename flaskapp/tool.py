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


if __name__ == '__main__':
    mcp.run(transport='sse')
