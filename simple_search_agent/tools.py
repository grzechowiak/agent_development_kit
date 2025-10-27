
import requests

# ============================================================================
# TOOLS
# ============================================================================

def check_url_exists(url: str):
    """
    Checks if a given URL is valid. Tries HEAD first, then falls back to GET.
    Treats any 2xx or 3xx HTTP code as valid.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        r = requests.head(url, headers=headers, allow_redirects=True, timeout=5)
        if 200 <= r.status_code < 400:
            return True
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=6, stream=True)
        r.close()
        return 200 <= r.status_code < 400
    except Exception as e:
        print("Error checking URL:", e)
        return False
