"""
Retail Agent Orchestrator - Configuration Module

Loads environment variables and establishes the shared AutoGen LLM configuration
targeting Google Gemini models via Google's OpenAI-compatible endpoint.
"""

import os
import sys
from typing import Any, Dict
from dotenv import load_dotenv

# Ensure UTF-8 output handling for cross-platform terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Load environment variables from .env file
load_dotenv()


def get_llm_config(
    model: str | None = None,
    temperature: float = 0.2,
    seed: int | None = 42,
) -> Dict[str, Any]:
    """
    Constructs and returns the Microsoft AutoGen LLM configuration dictionary.
    
    Routes calls to Google Gemini using Google's OpenAI-compatible endpoint:
    https://generativelanguage.googleapis.com/v1beta/openai/
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "[WARNING] Neither GEMINI_API_KEY nor OPENAI_API_KEY is set in environment.\n"
            "   Please set GEMINI_API_KEY in your .env file or environment variables.\n"
            "   Example: GEMINI_API_KEY='your_api_key_here'",
            file=sys.stderr,
        )

    selected_model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    config_list = [
        {
            "model": selected_model,
            "api_key": api_key or "placeholder_key",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "temperature": temperature,
        }
    ]

    llm_config: Dict[str, Any] = {
        "config_list": config_list,
        "temperature": temperature,
    }

    if seed is not None:
        llm_config["cache_seed"] = seed

    return llm_config


# Shared default configuration instance
LLM_CONFIG = get_llm_config()
