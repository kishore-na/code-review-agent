# Code Review Agent

A lightweight command-line code review assistant built with `langgraph` and Anthropic Claude. The agent accepts either a file path or an inline code snippet, reviews the code for quality and performance issues, and returns structured findings.

## Features

- Review code from a local file path or inline text.
- Supports many common languages (`.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.cpp`, `.c`, `.html`, `.css`, `.sql`, `.sh`, etc.).
- Uses a directed state graph to route input, parse code, call Anthropic Claude, and format output.
- Returns findings in a human-readable code review summary.

## Repository Structure

- `main.py` - CLI entry point for interacting with the agent.
- `requirements.txt` - Python dependencies.
- `agent/graph.py` - Builds the review state graph and manages node flow.
- `agent/nodes.py` - Implements the router, file reader, inline parser, review request, and output formatter.
- `agent/tools.py` - File loading and language detection utilities.
- `agent/prompts.py` - System prompt and review prompt builder for the LLM.
- `agent/state.py` - Typed state definition for the graph.

## Requirements

- Python 3.11 or later
- `pip` package manager
- An Anthropic API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-org>/code-review-agent.git
cd code-review-agent
```

2. Create a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your Anthropic API key in the environment.

For macOS/Linux:

```bash
export ANTHROPIC_API_KEY="your_api_key"
```

For Windows (PowerShell):

```powershell
$env:ANTHROPIC_API_KEY = "your_api_key"
```

Optionally, create a `.env` file with the same variable and the app will load it automatically.

## Usage

Run the CLI:

```bash
python main.py
```

Then enter one of:

- A file path to review a source file.
- A code snippet directly.
- A fenced code block like:

```markdown
```python
print("Hello")
```
```

Type `exit` to quit.

Example session:

```text
Code Review Agent
────────────────────────
Paste a file path or code snippet.
Type 'exit' to quit.

>>> ./example.py

Code review — `example.py`
────────────────────────
Line    8  ⚠️  WARN  [QUALITY]  Function is missing a docstring.
────────────────────────
1 issue(s) found.
```

## How it Works

1. `main.py` loads the graph and reads user input.
2. `agent/graph.py` builds a `StateGraph` with nodes for routing, file reading, inline parsing, review, and formatting.
3. `agent/nodes.py` decides if the input is a file path or inline code.
4. If a file path is provided, `agent/tools.py` reads the file and detects its language.
5. The agent sends the code to Anthropic Claude with a structured prompt.
6. The response is parsed and formatted into line-based review findings.

## Supported Languages

The agent currently recognizes these file extensions:

- `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.cs`, `.java`, `.go`, `.rs`, `.cpp`, `.c`, `.html`, `.css`, `.sql`, `.sh`

If no extension is recognized, the code is treated as `plaintext`.

## Notes

- This project requires an Anthropic Claude model and an active API key.
- The system prompt instructs the model to return only JSON output.
- If the model returns fenced JSON or extra text, the code attempts to clean and parse it.

## License

This repository does not include a license file. Add a license if you plan to publish or share it publicly.
