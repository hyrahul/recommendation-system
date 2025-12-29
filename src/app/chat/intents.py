# app/chat/intents.py
from typing import Literal

ChatIntent = Literal[
    "RECOMMENDATION",
    "KNOWLEDGE",
    "MIXED",
    "UNCLEAR"
]
