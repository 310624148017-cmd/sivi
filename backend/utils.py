import os
import re
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [SIVI] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("sivi")

def get_base_dir() -> str:
    """Returns absolute path to the SIVI root directory"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_data_dir() -> str:
    """Returns absolute path to the SIVI data directory"""
    return os.path.join(get_base_dir(), "data")

def get_timestamp() -> str:
    """Returns ISO 8601 formatted timestamp"""
    return datetime.now().isoformat()

def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Robustly parses JSON from LLM outputs, handling markdown ```json blocks
    or raw embedded json objects.
    """
    if not text:
        return None
        
    text = text.strip()
    
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting inside ```json ... ``` or ``` ... ```
    code_block_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try extracting first outer matching { ... }
    curly_match = re.search(r'(\{[\s\S]*\})', text)
    if curly_match:
        try:
            return json.loads(curly_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    return None

def estimate_tokens(text: str) -> int:
    """Rough estimate of token count (1 token ~= 4 chars)"""
    return max(1, len(text) // 4)
