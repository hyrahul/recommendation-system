from enum import Enum


class ChatIntent(str, Enum):
    RECOMMENDATION = "RECOMMENDATION"
    KNOWLEDGE = "KNOWLEDGE"
    MIXED = "MIXED"
    UNCLEAR = "UNCLEAR"
