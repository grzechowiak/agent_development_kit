from pydantic import BaseModel, Field
from typing import Literal #List


# # ============================================================================
# # STRUCTURED OUTPUT SCHEMA - Define your exact JSON structure
# # ============================================================================

class URLResult(BaseModel):
    """Structured output for a single movie"""
    title_from_user: str = Field(description="Movie title originally as provided by the user'")
    url: str = Field(description="The provided URL or 'not_found'")
    url_validated: Literal["Yes", "No", "Not Found"] = Field(description="Whether URL was validated by the tool itself")

# # To be implemented in the future
# # class MultipleURLResults(BaseModel):
# #     """Structured output for multiple movies"""
# #     results: List[URLResult] = Field(description="List of movie results")