import requests
from typing import Literal
from google.adk.tools import ToolContext
from crewai_tools import SerperDevTool
from config_shared import StateVariables as sv

# ============================================================================
# HELPER TOOLS
# ============================================================================

ValidationStatus = Literal["valid_validation", "invalid_validation", "not_found"]
def exit_loop(tool_context: ToolContext, *, status: ValidationStatus ):
    """
    Persist the final validation status and (if valid) the current URL as the final URL,
    then escalate to terminate the LoopAgent.
    Allowed values:
      - "valid_validation"
      - "invalid_validation"
      - "not_found"
    """
    print(f"[exit_loop] called by {tool_context.agent_name} with status={status}")

    # Save status exactly as used by the validator / formatter
    tool_context.state[sv.STATE_VALIDATION_RESULT] = status

    # If success, persist the vetted URL as final
    cur_url = tool_context.state.get(sv.STATE_CURRENT_URL)
    if isinstance(cur_url, str) and status == "valid_validation":
        tool_context.state[sv.STATE_FINAL_URL] = cur_url

    # Terminate the loop
    tool_context.actions.escalate = True
    print("[exit_loop] escalate=True set")
    return {"status": status}

# ============================================================================
# MAIN TOOLS
# ============================================================================
## URL Checker
def check_url_exists(url: str) -> Literal["valid_url", "invalid_url"]:
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
            return "valid_url"
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=6, stream=True)
        r.close()
        return "valid_url" if 200 <= r.status_code < 400 else "invalid_url"
    except Exception as e:
        print("Error checking URL:", e)
        return "invalid_url"


## Serper Internet Search Tool
serper_tool_instance = SerperDevTool(
    n_results=5,
    save_file=False,
    search_type="search",
)

def internet_search(query: str) -> str:
    """
    Searches the internet for a given query and returns the results.
    Use this to find specific URLs.
    The input must be a single string representing the search query.
    """
    # Call the underlying tool with the specific keyword argument it expects.
    return serper_tool_instance.run(search_query=query)
