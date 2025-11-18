# External Libraries
from google.adk.agents import SequentialAgent#, LoopAgent
# From other Agents
from web_search_loop_agent.agent import root_agent as iterative_url_finder_pipeline
from web_scraping_agent.agent import root_agent as scraping_agent

# ============================================================================
# ROOT AGENT: Sequential pipeline
# ============================================================================
root_agent = SequentialAgent(
    name="Full_Workflow_Agent",
    sub_agents=[
        iterative_url_finder_pipeline,
        scraping_agent
    ],
    description="Find, validate the URLs, format them and scrape the VOD results."
)