# ############# Agents Flow: #############
# root_agent (greeting_agent) - CONDITIONAL GATEKEEPER
#   └── title_extractor_agent [saves to STATE_MOVIE_TITLE]
#   └── movie_processing_pipeline (SequentialAgent)
#        ├── iterative_url_finder_pipeline
#        └── scraping_agent
#########################################

# External Libraries
from google.adk.agents import SequentialAgent, Agent
from google.adk.tools.agent_tool import AgentTool
# From other Agents
from web_search_loop_agent.agent import root_agent as iterative_url_finder_pipeline
from web_scraping_agent.agent import root_agent as scraping_agent
from root_workflow_agent.config import ModelsUsed as mdls
from root_workflow_agent.agent_instructions import TITLE_EXTRACTOR_INSTRUCTION, GREETING_AGENT_INSTRUCTION
from config_shared import StateVariables as sv

# ============================================================================
# AGENT 2: Sequential pipeline (search + scrape)
# ============================================================================
movie_processing_pipeline = SequentialAgent(
    name="WorkflowAgent",
    sub_agents=[
        iterative_url_finder_pipeline,
        scraping_agent
    ],
    description="Find, validate the URLs, format them and scrape the VOD results."
)

# ============================================================================
# AGENT 1: Title Extractor (extracts and saves movie title)
# ============================================================================
title_extractor_tool_agent = Agent(
    model=mdls.MAIN_MODEL,
    name='TitleExtractorToolAgent',
    description='Extracts the movie title from the user query',
    instruction=TITLE_EXTRACTOR_INSTRUCTION,
    output_key=sv.STATE_MOVIE_TITLE,
)

# ============================================================================
# AGENT 0: ROOT AGENT: Greeting Agent (handles conversation flow)
# ============================================================================
root_agent = Agent(
    model=mdls.MAIN_MODEL,
    name='MainGreetingAgent',
    description='Greets the user and routes to title extraction when appropriate',
    instruction=GREETING_AGENT_INSTRUCTION,
    tools = [AgentTool(agent=title_extractor_tool_agent)],
    sub_agents=[movie_processing_pipeline]
    # sub_agents=[title_extractor_agent, movie_processing_pipeline]
)