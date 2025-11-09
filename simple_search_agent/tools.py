
# Helper Tools
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext
# Main Tools
import requests
from crewai_tools import SerperDevTool


# ============================================================================
# HELPER TOOLS
# ============================================================================
STATE_ATTEMPT_COUNT = "attempt_count"

# --- Tool Definition ---
def exit_loop(tool_context: ToolContext, *, status: str = "valid"):
    """
    Signal the loop to exit AND persist a final status in shared state.
    status: "valid" | "not_found"
    """
    # Persist finalization info for downstream agents
    cur_url = tool_context.state.get("current_url")
    if cur_url:
        tool_context.state["final_url"] = cur_url
    tool_context.state["validation_result"] = status
    tool_context.actions.escalate = True
    return {"status": status}


def increment_attempt(tool_context: ToolContext):
    raw = tool_context.state.get(STATE_ATTEMPT_COUNT)
    current_count = raw if isinstance(raw, int) and raw >= 0 else 0
    new_val = current_count + 1
    tool_context.state[STATE_ATTEMPT_COUNT] = new_val
    return {"attempt_count": new_val}


def _reset_loop_state(callback_context: CallbackContext):
    callback_context.state["current_url"] = None
    callback_context.state["validation_result"] = None
    callback_context.state["final_url"] = None
    callback_context.state["attempt_count"] = 0



# ============================================================================
# MAIN TOOLS
# ============================================================================
## URL Checker
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


## Serper Internet Search Tool
serper_tool_instance = SerperDevTool(
    n_results=10,
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
