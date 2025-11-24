# External Libraries
from google.adk.agents import Agent, LoopAgent, SequentialAgent
# Shared Module
from config_shared import StateVariables as sv ## Load state variables from the main workflow
# Internal Modules
from web_search_loop_agent.agent_instructions import (
    SEARCH_AGENT_INSTRUCTION, VALIDATOR_AGENT_INSTRUCTION, TITLE_EXTRACTOR_INSTRUCTION, FORMATTING_AGENT_INSTRUCTION)
from web_search_loop_agent.tools import internet_search, check_url_exists, exit_loop
from web_search_loop_agent.callbacks import increment_attempt, _reset_loop_state
from web_search_loop_agent.structured_outputs import URLResult
from web_search_loop_agent.config import AgentsNames as agnt
from web_search_loop_agent.config import ModelsUsed as mdls


# # ============================================================================
# # AGENT 0: Title Extractor (runs first)
# # ============================================================================
# title_extractor_agent = Agent(
#     model=mdls.MAIN_MODEL,
#     name=agnt.agent_title_extractor,
#     description='Extracts the movie title from the user query',
#     instruction=TITLE_EXTRACTOR_INSTRUCTION,
#     output_key=sv.STATE_MOVIE_TITLE
# )

# ============================================================================
# SUB-AGENT 1A: Search Agent (runs inside LoopAgent)
# ============================================================================

search_agent = Agent(
    model=mdls.MAIN_MODEL,
    name=agnt.agent_search,
    description='Finds a JustWatch URL over multiple attempts using web search.',
    instruction=SEARCH_AGENT_INSTRUCTION,
    # before_agent_callback = increment_attempt, ## Consider using `increment_attempt` here
    tools=[internet_search, increment_attempt],
    output_key=sv.STATE_CURRENT_URL
)

# ============================================================================
# SUB-AGENT 1B: Validator Agent (runs inside LoopAgent)
# ============================================================================
validator_agent = Agent(
    model=mdls.MAIN_MODEL,
    name=agnt.agent_URL_validator,
    description='Validates JustWatch URLs using the check_url_exists tool',
    instruction=VALIDATOR_AGENT_INSTRUCTION,
    tools=[check_url_exists, exit_loop],
    output_key=sv.STATE_VALIDATION_RESULT,
)

# ============================================================================
# WORKFLOW AGENT 1: Loop agent that orchestrates the search (1A) and validation (1B)
# ============================================================================
refinement_loop = LoopAgent(
    name=agnt.agent_refinement_loop,
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
    model=mdls.MAIN_MODEL,
    name=agnt.agent_formatter,
    description='Accepts URL links which were found and validated, and formats them into the final output schema',
    instruction=FORMATTING_AGENT_INSTRUCTION,
    output_schema = URLResult, ## When using output_schema -> cannot use tools at the same time
    output_key=sv.STATE_FINAL_URL
)


# ============================================================================
# ROOT AGENT: Sequential pipeline
# ============================================================================
root_agent = SequentialAgent(
    name="IterativeURLFinderPipeline",
    sub_agents=[
        # title_extractor_agent,
        refinement_loop,
        formatting_agent,
    ],
    description="Find and validated the URLs, and later format them"
)