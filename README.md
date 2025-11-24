# StreamAgent

## 📋 Desc.
A Python-based multi-agent system designed to find relevant streaming sources for a given movie and determine where it's currently available. This project leverages Google's Agent Development Kit (ADK) to power its search.

## ⚙️Architecture
*While still in progress, the current architecture looks like follow:*
```
01.root_agent (MainGreetingAgent with 1 sub-agent)
|    ├── title_extractor_agent (Tool Agent)
│        └── [saves to STATE_MOVIE_TITLE]
│
└ 01.1. movie_processing_pipeline (SequentialAgent with 2 sub-agents)
    │
    ├── 02. iterative_url_finder_pipeline (SequentialAgent with 2 sub-agents)
    │   │
    │   ├── 02.1.refinement_loop (LoopAgent - with 2 sub-agents)
    │   │   │
    │   │   ├── 02.1.1. search_agent
    │   │   │   ├── Tool: internet_search
    │   │   │   ├── Tool: increment_attempt
    │   │   │   └── [saves to STATE_CURRENT_URL]
    │   │   │
    │   │   └── 02.1.2. validator_agent
    │   │       ├── Tool: check_url_exists
    │   │       ├── Tool: exit_loop
    │   │       └── [saves to STATE_FINAL_URL, STATE_VALIDATION_RESULT]
    │   │
    │   └── 02.2. formatting_agent
    │       ├── Reads: STATE_MOVIE_TITLE, STATE_FINAL_URL, STATE_VALIDATION_RESULT
    │       └── Output Schema: URLResult
    │
    └── 03. Web_Scraping_Agent (with 1 sub-agent)
        │   ├── Tool: web_scraping_tool (Playwright + BeautifulSoup)
        │   └── [returns provider_names]
        │
        └── 03.1. Sub-Agent: vod_formatting_agent
            ├── Input: provider_names list
            └── Output Schema: MultipleVODResult
```

https://github.com/user-attachments/assets/77411951-1741-4d57-be48-f5304954c2d8

---

## 🚀 Getting Started

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. Using Poetry ensures that you can easily replicate the exact development environment.

1.  **Install Poetry** (if you don't have it):
    Follow the instructions on the [official website](https://python-poetry.org/docs/#installation).

2.  **Clone the repository and navigate to the project directory:**
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```
    
3.  **Install the dependencies:**
    ```bash
    poetry install
    ```
    This will create a virtual environment and install all the necessary packages from the `poetry.lock` file to ensure a reproducible setup.

4.  **Run the application:**
    Use `poetry run` to execute scripts within the project's virtual environment.
    ```bash
    poetry run python your_main_script.py
    ```
