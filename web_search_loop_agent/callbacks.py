from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext
from config_shared import StateVariables as sv

# ============================================================================
# Callbacks
# ============================================================================

def _reset_loop_state(callback_context: CallbackContext):
    callback_context.state[sv.STATE_CURRENT_URL] = None
    callback_context.state[sv.STATE_FINAL_URL] = None
    callback_context.state[sv.STATE_VALIDATION_RESULT] = None
    callback_context.state[sv.STATE_ATTEMPT_COUNT] = 0


def increment_attempt(tool_context: ToolContext):
    raw = tool_context.state.get(sv.STATE_ATTEMPT_COUNT)
    current_count = raw if isinstance(raw, int) and raw >= 0 else 0
    new_val = current_count + 1
    tool_context.state[sv.STATE_ATTEMPT_COUNT] = new_val
    return {sv.STATE_ATTEMPT_COUNT: new_val}