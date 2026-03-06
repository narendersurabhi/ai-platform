"""Response parsing utilities."""
from dataclasses import dataclass


@dataclass
class ParsedResponse:
    answer: str


def parse_response(raw_text: str) -> ParsedResponse:
    return ParsedResponse(answer=raw_text.strip())
