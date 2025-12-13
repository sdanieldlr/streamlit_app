
import os # Lets you interact with files, folders, and environment variables
from openai import OpenAI # openai is the official Python client library for the OpenAI API (installed it with pip install openai), we use "OpenAI" for the functions
# os gets API keys, openai connects to the AI API

# llm_utils.py
# Handles AI features: summarize / sentiment / keywords / chat


MODEL = "gpt-4o-mini"   # model used


def _get_api_key():
    """
    1) Try environment variable OPENAI_API_KEY
    2) If not found, try secrets.py (local file, not in git)
    """
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key

    try:
        #We create secrets.py with:  OPENAI_API_KEY = "sk-...."
        from secrets import OPENAI_API_KEY  # type: ignore
        return OPENAI_API_KEY
    except Exception:
        return None


def _get_client():
    """Return an OpenAI client, or None if no API key is configured."""
    api_key = _get_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _basic_call(system_prompt: str, user_input: str) -> str:
    """
    Helper function: sends text to the model and returns its reply as a string.
    Used by summarize_text, analyze_sentiment and extract_keywords.
    """
    client = _get_client()
    if client is None:
        return (
            "[LLM not configured] Set OPENAI_API_KEY as an environment "
            "variable or create secrets.py with OPENAI_API_KEY."
        )

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM error] {e}"


#Public functions used by Streamlit#

def summarize_text(text: str) -> str:
    """Return a short summary of the text."""
    system = (
        "You help users summarize their notes. "
        "Write a short, clear summary in simple, natural language."
    )
    return _basic_call(system, text)


def analyze_sentiment(text: str) -> str:
    """
    Return the sentiment of the text.
    Example: 'Overall sentiment: positive (short explanation...)'
    """
    system = (
        "You analyse the overall feeling of the text. "
        "Say whether it is positive, negative or neutral and explain briefly."
    )
    return _basic_call(system, text)


def extract_keywords(text: str) -> list[str]:
    """
    Extract main keywords from the text.
    The model is asked to return ONLY a comma-separated list.
    We split it into a normal Python list before returning.
    """
    system = (
        "You pick out the most important words or short phrases from the text. "
        "Return ONLY those keywords as a comma-separated list, no extra text."
    )
    raw = _basic_call(system, text)
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return parts


def chat_reply(message: str, history: list[dict] | None = None) -> str:
    """
    Simple chatbot reply.

    history is a list of previous messages:
        [{"role": "user", "content": "hi"},
         {"role": "assistant", "content": "hello"}]
    """
    if history is None:
        history = []

    client = _get_client()
    if client is None:
        return (
            "[LLM not configured] Set OPENAI_API_KEY as an environment "
            "variable or create secrets.py with OPENAI_API_KEY."
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly, helpful assistant inside a notes app. "
                "Answer in a natural, simple way. Be short and to the point."
            ),
        },
        *history,
        {"role": "user", "content": message},
    ]

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.6,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM error] {e}"