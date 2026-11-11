"""Central config for optional external medicine APIs.

Keys are read from environment variables ONLY — never hardcode a real key
in source code. Copy `.env.example` to `.env` (or set env vars in your
host) and fill in what you have. Everything works without any key:
RxNav and OpenFDA are usable key-free; a key only raises rate limits.
Gemini (AI scan) needs a key to be enabled.
"""
import os

def _load_dotenv():
    """Tiny .env loader (stdlib only, no python-dotenv dependency)."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except OSError:
        pass

_load_dotenv()

# Optional keys (empty = not configured, app falls back to local data)
OPENFDA_API_KEY = os.environ.get("OPENFDA_API_KEY", "").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
TINYFISH_API_KEY = os.environ.get("TINYFISH_API_KEY", "").strip()
# Generic fallback if you use a different provider later
CURAMED_API_KEY = os.environ.get("CURAMED_API_KEY", "").strip()

def api_status():
    """Safe status for /api/config/status — never returns the key itself."""
    return {
        "openfda_configured": bool(OPENFDA_API_KEY),
        "gemini_configured": bool(GEMINI_API_KEY),
        "tinyfish_configured": bool(TINYFISH_API_KEY),
        "generic_configured": bool(CURAMED_API_KEY),
        "rxnav": "always available (no key needed)",
        "tinyfish": "web search, needs key (free 12k searches/day)",
    }
