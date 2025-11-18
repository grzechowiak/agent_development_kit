# External Libraries
from google.adk.agents import SequentialAgent#, LoopAgent
# From other Agents
from web_search_loop_agent.agent import root_agent as IterativeURLFinderPipeline
from web_scraping_agent.agent import root_agent as scraping_agent

# Internal Modules
# from root_workflow_agent.tools import (
#     check_url_exists,
#     internet_search,
#     exit_loop
# )
# from root_workflow_agent.callbacks import (
#     _reset_loop_state,
#     increment_attempt
# )
# from root_workflow_agent.structured_outputs import URLResult
# from root_workflow_agent.agent_instructions import (
    # SEARCH_AGENT_INSTRUCTION,
    # FORMATTING_AGENT_INSTRUCTION,
    # VALIDATOR_AGENT_INSTRUCTION,
    # TITLE_EXTRACTOR_INSTRUCTION
# )
# from root_workflow_agent.config import StateVariables as sv
# from config_shared import AgentsNames as agnt
# from root_workflow_agent.config import ModelsUsed as mdls



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

# # ============================================================================
# # SUB-AGENT 1A: Search Agent (runs inside LoopAgent)
# # ============================================================================
#
# search_agent = Agent(
#     model=mdls.MAIN_MODEL,
#     name=agnt.agent_search,
#     description='Finds a JustWatch URL over multiple attempts using web search.',
#     instruction=SEARCH_AGENT_INSTRUCTION,
#     # before_agent_callback = increment_attempt, ## Consider using `increment_attempt` here
#     tools=[internet_search, increment_attempt],
#     output_key=sv.STATE_CURRENT_URL
# )
#
# # ============================================================================
# # SUB-AGENT 1B: Validator Agent (runs inside LoopAgent)
# # ============================================================================
# validator_agent = Agent(
#     model=mdls.MAIN_MODEL,
#     name=agnt.agent_URL_validator,
#     description='Validates JustWatch URLs using the check_url_exists tool',
#     instruction=VALIDATOR_AGENT_INSTRUCTION,
#     tools=[check_url_exists, exit_loop],
#     output_key=sv.STATE_VALIDATION_RESULT,
# )
#
# # ============================================================================
# # WORKFLOW AGENT 1: Loop agent that orchestrates the search (1A) and validation (1B)
# # ============================================================================
# refinement_loop = LoopAgent(
#     name=agnt.agent_refinement_loop,
#     sub_agents=[
#         search_agent,
#         validator_agent,
#     ],
#     before_agent_callback=_reset_loop_state,
#     max_iterations=3,
# )

# # ============================================================================
# # AGENT 2: Formatting agent (runs after loop completes)
# # ============================================================================
# formatting_agent = Agent(
#     model=mdls.MAIN_MODEL,
#     name=agnt.agent_formatter,
#     description='Accepts URL links which were found and validated, and formats them into the final output schema',
#     instruction=FORMATTING_AGENT_INSTRUCTION,
#     output_schema = URLResult ## When using output_schema -> cannot use tools at the same time
# )

# ============================================================================
# ROOT AGENT: Sequential pipeline
# ============================================================================
root_agent = SequentialAgent(
    name="Full_Workflow_Agent",
    sub_agents=[
        IterativeURLFinderPipeline,
        scraping_agent
    ],
    description="Find, validate the URLs, later format them and scrape the VOD results."
)