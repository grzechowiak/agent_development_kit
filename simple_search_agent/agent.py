# External Libraries
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search

# Internal Modules
from simple_search_agent.tools import check_url_exists
from simple_search_agent.structured_outputs import MultipleURLResults
from simple_search_agent.config import (
    model_to_use
)
from simple_search_agent.agent_instructions import (
    SEARCH_AGENT_INSTRUCTION,
    ROOT_AGENT_INSTRUCTION)


# ============================================================================
# AGENT 1: Dedicated agent for the built-in google_search tool (Agent as a tool)
# ============================================================================

search_agent = Agent(
    model=model_to_use,
    name='justwatch_searcher',
    description='Searches Google for JustWatch movie pages',
    instruction=SEARCH_AGENT_INSTRUCTION,
    tools=[google_search],  # Agent using one built-in tool
)

# ============================================================================
# AGENT 2: Root agent that orchestrates the search and validation
# ============================================================================

root_agent = Agent(
    model=model_to_use,
    name='justwatch_link_finder',
    description='Finds and validates JustWatch movie page URLs',
    instruction=ROOT_AGENT_INSTRUCTION,
    # Wrapping `the search_agent` as an AgentTool due to ADK's limitations
    # The root agent uses the search_agent (as a tool) and a custom function - currently ADK doesn't support build-in tools + custom tools
    tools=[AgentTool(agent=search_agent), check_url_exists],
    output_schema = MultipleURLResults
)
