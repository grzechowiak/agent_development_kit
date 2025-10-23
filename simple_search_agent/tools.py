
import requests

# ============================================================================
# TOOLS
# ============================================================================

def check_url_exists(url: str):
    """
    Checks if a given URL is valid by sending a HEAD request.

    Args:
        url: The full URL string to validate.
    """
    try:
        # Set a user-agent to mimic a browser, as some sites block default script agents
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=5)
        if 200 <= response.status_code < 300:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL {url}: {e}")
        return False
