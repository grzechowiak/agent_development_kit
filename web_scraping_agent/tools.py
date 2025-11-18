# External Libraries
import os
from firecrawl import FirecrawlApp


# ============================================================================
# MAIN TOOLS
# ============================================================================
## URL Scrapper (FireCrawl)

# Initialize Firecrawl
firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Scraping function
def scrape_website(url: str):
    """Scrapes a website and returns the content in markdown format"""
    result = firecrawl.scrape(url, formats=['markdown'])
    # Extract markdown from the result
    if hasattr(result, 'markdown'):
        return result.markdown
    return str(result)