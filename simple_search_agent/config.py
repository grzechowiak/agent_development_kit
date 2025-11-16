
class ModelsUsed:
    # MAIN_MODEL='gemini-2.5-pro'
    # MAIN_MODEL ='gemini-2.5-flash'
    # MAIN_MODEL ="gemini-2.5-flash-lite"
    # MAIN_MODEL = "gemini-2.5-flash-lite-preview-09-2025"
    MAIN_MODEL = "gemini-2.0-flash"
    # MAIN_MODEL = "gemini-2.0-flash-lite"

# --- State Keys ---
class StateVariables:
    STATE_MOVIE_TITLE = "movie_title"
    STATE_CURRENT_URL = "current_url"
    STATE_FINAL_URL = 'final_url'
    STATE_VALIDATION_RESULT = "validation_result"
    STATE_ATTEMPT_COUNT = "attempt_count"


class AgentsNames:
    agent_title_extractor = "TitleExtractor"
    agent_search = "justwatch_search_agent"
    agent_URL_validator = "URLValidator"
    agent_refinement_loop = "RefinementLoop"
    agent_formatter = "FinalFormatter"
    the_main_root_agent = "IterativeURLFinderPipeline"