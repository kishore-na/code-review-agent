import os

EXTENSION_TO_LANGUAGE = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".cs": "csharp",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp",
    ".c": "c",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".sh": "bash",
}

def read_file(path: str) -> dict:
    expanded = os.path.expanduser(path.strip())

    if not os.path.exists(expanded):
        raise FileNotFoundError(f"No file found at: {expanded}")

    if not os.path.isfile(expanded):
        raise ValueError(f"Path is a directory, not a file: {expanded}")

    _, ext = os.path.splitext(expanded)
    language = EXTENSION_TO_LANGUAGE.get(ext.lower(), "plaintext")
    filename = os.path.basename(expanded)

    with open(expanded, "r", encoding="utf-8") as f:
        code = f.read()

    if not code.strip():
        raise ValueError(f"File is empty: {expanded}")

    return {
        "code": code,
        "filename": filename,
        "language": language,
    }