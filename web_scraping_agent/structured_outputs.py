from pydantic import BaseModel, Field
from typing import List

# ============================================================================
# STRUCTURED OUTPUT SCHEMA - Define your exact JSON structure
# ============================================================================

class VODResult(BaseModel):
    """Structured output for a single movie"""
    VOD_source: str = Field(description="The name of the VOD platform, eg. Netflix, HBO, etc.")

class MultipleVODResult(BaseModel):
    """Structured output for multiple movies"""
    results: List[VODResult] = Field(description="List of VOD platforms")