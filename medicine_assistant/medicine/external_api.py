"""Optional live medicine APIs (RxNav + OpenFDA + Gemini vision).

Design rules (same as the rest of Medsathi):
- Works with NO key (RxNav/OpenFDA key-free mode).
- Never raises to the caller: on any network/API error returns [] / None
  so the app always falls back to the local database.
- Never logs or returns API keys.
"""
import base64
import json
import urllib.parse
import urllib.request

from config import OPENFDA_API_KEY, GEMINI_API_KEY, TINYFISH_API_KEY

TIMEOUT = 8  # seconds — keep the UI responsive


def _get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Medsathi/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def search_rxnav(query):
    """RxNav name search -> [{name, rxcui}]. No key needed."""
    q = urllib.parse.quote(query.strip())
    if not q:
        return []
    try:
        data = _get_json(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={q}")
        ids = (data.get("idGroup") or {}).get("rxcui") or []
        out = []
        for rxcui in ids[:8]:
            try:
                props = _get_json(f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}.json")
                p = (props.get("rxcuiProperties") or {})
                out.append({
                    "name": p.get("name", query),
                    "rxcui": rxcui,
                    "generic": p.get("name", query),
                    "source": "RxNav (NLM, live)",
                })
            except Exception:
                continue
        return out
    except Exception:
        return []


def search_openfda(query):
    """OpenFDA drug label search. Key optional (higher limits with key)."""
    q = urllib.parse.quote(query.strip())
    if not q:
        return []
    # OpenFDA documents api_key as the first parameter, before search/limit.
    auth = f"api_key={urllib.parse.quote(OPENFDA_API_KEY)}&" if OPENFDA_API_KEY else ""
    url = f"https://api.fda.gov/drug/label.json?{auth}search=openfda.brand_name:{q}&limit=5"
    try:
        data = _get_json(url)
        out = []
        for r in (data.get("results") or [])[:5]:
            openfda = r.get("openfda") or {}
            brand = (openfda.get("brand_name") or [query])[0]
            generic = (openfda.get("generic_name") or [""])[0]
            out.append({
                "name": brand,
                "generic": generic,
                "uses": (r.get("indications_and_usage") or [""])[0][:300],
                "source": "OpenFDA (live)",
            })
        return out
    except Exception:
        return []


def search_tinyfish(query, location="IN", language="en"):
    """TinyFish search API -> ranked web results. Needs TINYFISH_API_KEY."""
    if not TINYFISH_API_KEY or not query or not query.strip():
        return []
    params = urllib.parse.urlencode({
        "query": f"{query.strip()} medicine uses dosage side effects",
        "purpose": "Identify a medicine from its name and summarise approved uses, dose and warnings",
        "location": location,
        "language": language,
    })
    req = urllib.request.Request(
        f"https://api.search.tinyfish.ai?{params}",
        headers={
            "X-API-Key": TINYFISH_API_KEY,
            "Accept": "application/json",
            "User-Agent": "Medsathi/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
        out = []
        for r in (data.get("results") or [])[:6]:
            out.append({
                "name": r.get("title") or query,
                "generic": "",
                "manufacturer": r.get("site_name", ""),
                "uses": (r.get("snippet") or "")[:300],
                "url": r.get("url", ""),
                "source": "TinyFish (live web)",
            })
        return out
    except Exception:
        return []


def search_external(query):
    """Combined live search. Returns [] if offline / no results."""
    if not query or not query.strip():
        return []
    results = search_rxnav(query) + search_openfda(query) + search_tinyfish(query)
    # de-dupe by lowercase name, keep order
    seen, out = set(), []
    for r in results:
        key = (r.get("name") or "").lower()
        if key and key not in seen:
            seen.add(key)
            out.append(r)
    return out[:10]


def scan_with_gemini(image_b64, mime="image/jpeg"):
    """Send a label photo to Gemini vision -> extracted medicine name text.

    Returns the recognized text, or None if no key / API error (caller
    then falls back to on-device OCR).
    """
    if not GEMINI_API_KEY or not image_b64:
        return None
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    )
    payload = {
        "contents": [{
            "parts": [
                {"text": "Read this medicine label photo. Reply with ONLY the medicine name, brand name, strength and dosage form printed on it, one per line. Do not add explanations. If unreadable, reply with nothing."},
                {"inline_data": {"mime_type": mime, "data": image_b64}},
            ]
        }]
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
        text = (
            data["candidates"][0]["content"]["parts"][0]["text"]
        ).strip()
        return text or None
    except Exception:
        return None
