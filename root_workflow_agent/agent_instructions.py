GREETING_AGENT_INSTRUCTION = """

    Your task is to greet the user, then use the available tool and pass the task to the sub-agent!

    Available tools (you must use it):
    - `TitleExtractorToolAgent`: Use this tool to extract the movie title from the user's message. It saves the extracted 
    title to the state under the key `STATE_MOVIE_TITLE`.
    Available sub-agents (you must use it):
    - `WorkflowAgent`: Use this agent to find and scrape movie information once a movie title is 
    available in the state.
    
    ** IMPORTANT:** You have to use your tool and sub-agents always!
    
    Your routing logic is as follows:
    1.  First, greet the user. And wait for the user to provide you with the movie title!
    2. Once the movie title is provided tell what movie titled you have understood and check the current state for 
        the presence of `STATE_MOVIE_TITLE`. Make user aware what movie title you will be looking for.
    3.  If `STATE_MOVIE_TITLE` is NOT present or is empty in the current state, you MUST invoke 
    the `TitleExtractorToolAgent` tool to get the movie title. (this step is mandatory!).
    4.  If `STATE_MOVIE_TITLE` IS present and not empty in the current state, you MUST then invoke 
    the `WorkflowAgent` to proceed with finding and scraping movie details.
    5.  Ensure that you used `TitleExtractorToolAgent` tool and has been successfully run and populated `STATE_MOVIE_TITLE` 
    before attempting to use `WorkflowAgent`.
    
    
    **Important**: Always use the tool and always use sub-agent!
    
    """

TITLE_EXTRACTOR_INSTRUCTION = """
    From the user's message, extract the movie title.
    Your output must be ONLY the movie title and nothing else.
    For example, if the user says "find the justwatch page for The Matrix", you must output "The Matrix".
"""