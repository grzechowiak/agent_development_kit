
from pydantic import BaseModel, Field
from typing import List, Literal


# ============================================================================
# STRUCTURED OUTPUT SCHEMA - Define your exact JSON structure
# ============================================================================

class URLResult(BaseModel):
    """Structured output for a single movie"""
    title_from_user: str = Field(description="Movie title originally as provided by the user'")
    url: str = Field(description="JustWatch URL or 'not_found'")
    URL_fetched: Literal["success", "error"] = Field(description="Whether the search_agent found the URL successfully")
    url_validated: Literal["Yes", "No"] = Field(description="Whether URL was validated by the tool itself")

class MultipleURLResults(BaseModel):
    """Structured output for multiple movies"""
    results: List[URLResult] = Field(description="List of movie results")