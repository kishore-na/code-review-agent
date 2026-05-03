# Code Review Agent

A command-line AI agent that reviews source code for **quality and performance issues**, built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Anthropic Claude](https://www.anthropic.com).

---

## What it does

- Accepts a **file path** or **inline code snippet** as input
- Routes the input through a LangGraph state graph
- Sends code to Claude with a structured review prompt
- Returns **inline comments per issue**, grouped by line number with severity levels

Example output:

```
Code review — `users.py`
────────────────────────────────────────
Line    1  ℹ️  INFO     [QUALITY]      Function lacks a docstring.
Line    3  ⚠️  WARN     [QUALITY]      Variable 'id' shadows the built-in function — rename to 'user_id'.
Line    4  ❌ ERROR    [QUALITY]      SQL query uses string interpolation — use parameterized queries instead.
Line    4  ❌ ERROR    [PERFORMANCE]  Query executed inside a loop — batch IDs into a single IN clause.
────────────────────────────────────────
4 issue(s) found.
```

---

## How it works

The agent is a directed **LangGraph state graph** with 5 nodes:

```
user input
    │
    ▼
 router  ──── file path ────▶  read_file
    │                               │
    └──── inline code ──▶ use_inline
                                    │
                          ┌─────────┘
                          ▼
                     review_code   ◀── Claude (Anthropic API)
                          │
                          ▼
                    format_output
                          │
                          ▼
                         END
```

| Node | Role |
|---|---|
| `router` | Conditional node — detects file path vs inline code |
| `read_file` | Reads file from disk, detects language from extension |
| `use_inline` | Extracts code from fenced block or raw paste |
| `review_code` | Calls Claude, returns structured JSON findings |
| `format_output` | Formats findings into inline comments sorted by line |

---

## Stack

| | |
|---|---|
| Language | Python 3.12 |
| Agent framework | LangGraph |
| LLM | Anthropic Claude (claude-opus-4-5) |
| Config | python-dotenv |

---

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/kishore-na/code-review-agent.git
cd code-review-agent
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Add your Anthropic API key**

```bash
cp .env.example .env
# edit .env and add your key
```

`.env` format:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Usage

```bash
python main.py
```

**Review a file:**

```
>>> ~/projects/myapp/utils.py
```

**Review inline code** (type `--code`, paste, then `Ctrl+D`):

```
>>> --code
(Paste code, then press Enter + Ctrl+D when done)
def get_users(ids):
    result = []
    for id in ids:
        ...
^D
```

**Exit:**

```
>>> exit
```

---

## Supported languages

`.py` `.ts` `.tsx` `.js` `.jsx` `.cs` `.java` `.go` `.rs` `.cpp` `.c` `.html` `.css` `.sql` `.sh`

---

## Project structure

```
code-review-agent/
├── .env                  # API key (not committed)
├── .env.example          # Template
├── requirements.txt
├── main.py               # CLI entrypoint
└── agent/
    ├── state.py          # ReviewState TypedDict
    ├── prompts.py        # System prompt + review prompt builder
    ├── tools.py          # read_file utility + language detection
    ├── nodes.py          # All 5 node functions
    └── graph.py          # LangGraph graph assembly
```

---

## Roadmap

- [ ] Multi-file / directory support using LangGraph `Send` (map-reduce pattern)
- [ ] Agentic doc lookup — agent autonomously fetches fix patterns per finding
- [ ] Severity filter (`--errors-only` flag)
- [ ] Markdown report export