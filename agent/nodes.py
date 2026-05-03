import json
import re
import anthropic
from agent.state import ReviewState
from agent.tools import read_file
from agent.prompts import SYSTEM_PROMPT, build_review_prompt

def get_client():
    return anthropic.Anthropic()

# ── 1. router ────────────────────────────────────────────────────────────────

def router(state: ReviewState) -> dict:
    msg = state["user_message"].strip()
    # looks like a file path if it starts with /, ~, ./, ../ or ends with a known extension
    path_pattern = r'^[\/~\.]|.*\.(py|ts|tsx|js|jsx|cs|java|go|rs|cpp|c|sql|sh|html|css)$'
    if re.match(path_pattern, msg, re.IGNORECASE):
        return {"route": "file"}
    return {"route": "inline"}

# ── 2. read_file_node ─────────────────────────────────────────────────────────

def read_file_node(state: ReviewState) -> dict:
    path = state["user_message"].strip()
    result = read_file(path)  # plain call, not .invoke()
    return {
        "code": result["code"],
        "filename": result["filename"],
        "language": result["language"],
    }

# ── 3. use_inline_node ────────────────────────────────────────────────────────

def use_inline_node(state: ReviewState) -> dict:
    msg = state["user_message"]

    # pull code from fenced block if present: ```lang\n...\n```
    fenced = re.search(r'```(?:\w+)?\n(.*?)```', msg, re.DOTALL)
    if fenced:
        code = fenced.group(1).strip()
        # try to detect language from fence label e.g. ```python
        lang_match = re.search(r'```(\w+)', msg)
        language = lang_match.group(1).lower() if lang_match else "plaintext"
    else:
        code = msg.strip()
        language = "plaintext"

    return {
        "code": code,
        "filename": "inline",
        "language": language,
    }

# ── 4. review_code_node ───────────────────────────────────────────────────────

def review_code_node(state: ReviewState) -> dict:
    response = get_client().messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": build_review_prompt(
                    code=state["code"],
                    filename=state["filename"],
                    language=state["language"],
                ),
            }
        ],
    )

    raw = response.content[0].text.strip()
    print("RAW LLM OUTPUT:", raw)  # debug

    try:
        findings = json.loads(raw)
    except json.JSONDecodeError:
        # if the LLM wrapped in fences despite instructions, strip and retry
        cleaned = re.sub(r'```(?:json)?\n?', '', raw).strip('`').strip()
        findings = json.loads(cleaned)

    return {"findings": findings}

# ── 5. format_output_node ─────────────────────────────────────────────────────

SEVERITY_PREFIX = {
    "error":   "❌ ERROR",
    "warning": "⚠️  WARN",
    "info":    "ℹ️  INFO",
}

def format_output_node(state: ReviewState) -> dict:
    findings = state["findings"]
    filename = state["filename"]

    if not findings:
        return {"output": f"✅  No issues found in `{filename}`."}

    # sort by line number so comments read top-to-bottom
    sorted_findings = sorted(findings, key=lambda f: f.get("line", 0))

    lines = [f"Code review — `{filename}`\n{'─' * 40}"]

    for f in sorted_findings:
        prefix = SEVERITY_PREFIX.get(f["severity"], "•")
        category = f["category"].upper()
        line_no = f["line"]
        message = f["message"]
        lines.append(f"Line {line_no:>4}  {prefix}  [{category}]  {message}")

    lines.append(f"{'─' * 40}")
    lines.append(f"{len(sorted_findings)} issue(s) found.")

    return {"output": "\n".join(lines)}