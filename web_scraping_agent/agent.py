import os
from google.adk import Agent
from firecrawl import FirecrawlApp

from simple_search_agent.config import ModelsUsed as mdls


# Initialize Firecrawl
firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))


# Scraping function
def scrape_website(url: str):
    """Scrapes a website and returns the content in markdown format"""
    # For Firecrawl v2, use scrape with formats parameter
    result = firecrawl.scrape(url, formats=['markdown'])

    # Extract markdown from the result
    if hasattr(result, 'markdown'):
        return result.markdown
    return str(result)



root_agent  = Agent(
    model=mdls.MAIN_MODEL,
    name="web_scraping_agent_name",
    description='Extracts stream options from the user URL',
    instruction="You are a helpful assistant that can scrape websites when given a URL. Only information about the available VOD options (STREAM) are required to scrape, nothing else. Do not provide information about BUY, or RENT, only STRAM",
    tools=[scrape_website]
)

