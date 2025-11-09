# External Libraries
from google.adk.agents import Agent, SequentialAgent, LoopAgent
# from google.adk.tools.agent_tool import AgentTool
# from google.adk.tools import google_search
# from google.adk.tools.google_search_tool import GoogleSearchTool
# from google.adk.tools.tool_context import ToolContext

# Internal Modules
from simple_search_agent.tools import (
    check_url_exists,
    internet_search,
    exit_loop,
    increment_attempt,
    _reset_loop_state
)
from simple_search_agent.structured_outputs import MultipleURLResults
from simple_search_agent.config import (
    model_to_use
)
from simple_search_agent.agent_instructions import (
    SEARCH_AGENT_INSTRUCTION,
    FORMATTING_AGENT_INSTRUCTION,
    VALIDATOR_AGENT_INSTRUCTION,
    TITLE_EXTRACTOR_INSTRUCTION
)

# --- State Keys ---
STATE_MOVIE_TITLE = "movie_title"
STATE_CURRENT_URL = "current_url"
STATE_VALIDATION_RESULT = "validation_result"


# ============================================================================
# AGENT 0: Title Extractor (runs first)
# ============================================================================
title_extractor_agent = Agent(
    model=model_to_use,
    name='TitleExtractor',
    description='Extracts the movie title from the user query',
    instruction=TITLE_EXTRACTOR_INSTRUCTION,
    output_key=STATE_MOVIE_TITLE  # <-- THIS IS THE MAGIC!
    # The agent's output will be stored in state["movie_title"]
)

# ============================================================================
# SUB-AGENT 1A: Search Agent (runs inside LoopAgent)
# ============================================================================

search_agent = Agent(
    model=model_to_use,
    name='justwatch_search_agent', # Give it a unique name
    description='Finds a JustWatch URL over multiple attempts using web search.',
    instruction=SEARCH_AGENT_INSTRUCTION,
    # tools=[AgentTool(agent=search_agent_as_tool), increment_attempt],
    tools=[internet_search, increment_attempt],
    output_key=STATE_CURRENT_URL
)

# ============================================================================
# SUB-AGENT 1B: Validator Agent (runs inside LoopAgent)
# ============================================================================
validator_agent = Agent(
    model=model_to_use,
    name='URLValidator',
    description='Validates JustWatch URLs using the check_url_exists tool',
    instruction=VALIDATOR_AGENT_INSTRUCTION,
    tools=[check_url_exists, exit_loop],
    output_key=STATE_VALIDATION_RESULT,
    #include_contents='none'
)

# ============================================================================
# WORKFLOW AGENT 1: Loop agent that orchestrates the search (1A) and validation (1B)
# ============================================================================
refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        search_agent,
        validator_agent,
    ],
    before_agent_callback=_reset_loop_state,
    max_iterations=3,
)

# ============================================================================
# AGENT 2: Formatting agent (runs after loop completes)
# ============================================================================
formatting_agent = Agent(
    model=model_to_use,
    name='justwatch_link_formatter',
    description='Accepts URL links which were found and validated, and formats them into the final output schema',
    instruction=FORMATTING_AGENT_INSTRUCTION,
    # Wrapping `the search_agent` as an AgentTool due to ADK's limitations
    # The root agent uses the search_agent (as a tool) and a custom function - currently ADK doesn't support build-in tools + custom tools
    # sub_agents=[search_agent, validator_agent], ###<--- THIS IS NOT GOING TO WORK DUE TO LIMITATIONS oF ADK - BU IDK WHY ACTUALLY
    #tools=[AgentTool(agent=search_agent), AgentTool(agent=validator_agent)],
    output_schema = MultipleURLResults ## When using output_schema -> cannot use tools at the same time
)
# https://google.github.io/adk-docs/tools/function-tools/#key-aspects-of-this-example
# It's important to distinguish an Agent-as-a-Tool from a Sub-Agent.
#
#     Agent-as-a-Tool: When Agent A calls Agent B as a tool (using Agent-as-a-Tool), Agent B's answer is
#     passed back to Agent A, which then summarizes the answer and generates a response to the user.
#     Agent A retains control and continues to handle future user input.
#
#     Sub-agent: When Agent A calls Agent B as a sub-agent, the responsibility of answering the user is
#     completely transferred to Agent B. Agent A is effectively out of the loop. All subsequent user
#     input will be answered by Agent B.
#



# ============================================================================
# ROOT AGENT: Sequential pipeline
# ============================================================================
root_agent = SequentialAgent(
    name="IterativeURLFinderPipeline",
    sub_agents=[
        title_extractor_agent,
        refinement_loop,
        formatting_agent
    ],
    description="Find and validated the URLs, and later format them"
)