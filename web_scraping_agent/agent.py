# External Libraries
from google.adk import Agent
# Internal Modules
from web_scraping_agent.config import ModelsUsed as mdls
from web_scraping_agent.config import AgentsNames as agnt
from web_scraping_agent.structured_outputs import MultipleVODResult
from web_scraping_agent.tools import scrape_website
from web_scraping_agent.agent_instructions import WEB_SCARPING_AGENT_INSTRUCTION, VOD_FORMATTING_AGENT_INSTRUCTION


# ============================================================================
# AGENT 1: Web Scraper Agent
# ============================================================================
vod_formatting_agent = Agent(
    model=mdls.MAIN_MODEL,
    name=agnt.vod_agent_formatter,
    description='Your main task is to format the VOD result according to the given output schema.',
    instruction=VOD_FORMATTING_AGENT_INSTRUCTION,
    output_schema = MultipleVODResult ## When using output_schema -> cannot use tools at the same time
)

# ============================================================================
# ROOT AGENT: Web Scraper Agent
# ============================================================================
root_agent  = Agent(
    model = mdls.MAIN_MODEL,
    name = agnt.scraping_agent,
    description = 'Extracts stream options from the provided URL',
    instruction = WEB_SCARPING_AGENT_INSTRUCTION,
    sub_agents = [vod_formatting_agent],
    tools=[scrape_website]
)



