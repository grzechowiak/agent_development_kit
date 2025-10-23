# StreamAgent

A Python-based agentic solution designed to find relevant streaming sources for a given movie and determine where it's currently available. This project leverages Google's Agent Development Kit (ADK) to power its search.

*This project is currently in progress.*

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