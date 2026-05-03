from typing import TypedDict, Optional

class ReviewState(TypedDict, total=False):
    user_message: str
    code: str
    filename: str
    language: str
    findings: list[dict]
    output: str
    route: str