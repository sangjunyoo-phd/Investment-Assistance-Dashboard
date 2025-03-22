# Investment Assistance Dashboard

This project is an LLM tool built to assist in investment analysis and decision-making.
It leverages a **local large language model (LLM)** to provide brief results for investment research from natural language queries.
Implemented an **Evaluator-Optimizer Agentic Workflow** for reliable query result with small models and DuckDuckGoSearch to **fetch the up-to-date data**.

**Warning**:  Do not use it for actual investment decisions. The responsibility for any financial decisions rests solely with the user.

## Key Features:
* **Local LLM with Ollama** for cost free privacy.
* **Agentic Workflow** for efficient agent calls to gather data and perform analysis.
* **Up-to-Date Data** including stock prices, market news and reports, ensuring it always work with the most recent information.

## Prerequisites

Before running the project, you need to install the following:

- **[Poetry](https://python-poetry.org/docs/#installation)** for managing project dependencies.
- **[Ollama](https://ollama.com/download)** for running the local LLM models.


## Installation

1. **Clone the repository** to your preferred directory.

2. **Install Poetry** Follow the instruction on the [Official Poetry Website](https://python-poetry.org/docs/).

3. **Install Dependencies** Use your favorate terminal to go to the project directory, install the project dependencies

```bash
cd path\to\your\project\
poetry install
```


## Before running the app

1. **Ollama** should be installed an running

2. Pull model from Ollama from your terminal (ex. gemma3:4b)
```bash
ollama pull gemma3:4b
```

3. **Run the app** After installation, activate the Poetry virtual environment and run the app
```bash
poetry run streamlit run app.py
```