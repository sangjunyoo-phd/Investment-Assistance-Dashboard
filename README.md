# Investment Assistance Dashboard

This project is a Streamlit-based dashboard designed to assist with investment tracking and analysis.

---

## Prerequisites

Before running the project, you need to install the following:

- **[Poetry](https://python-poetry.org/docs/#installation)** for managing project dependencies.
- **[Ollama](https://ollama.com/download)** for running the local LLM models.

---

## Installation

1. **Clone the repository** to your preferred directory.

2. **Install Poetry** Follow the instruction on the [Official Poetry Website](https://python-poetry.org/docs/).

3. **Install Dependencies** Use your favorate terminal to go to the project directory, install the project dependencies

```bash
cd path\to\your\project\
poetry install
```

---

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

---