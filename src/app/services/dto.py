from dataclasses import dataclass
from typing import List, Optional, Literal
from app.db.models.lecture import Lecture

@dataclass
class RecommendationResult:
    status: Literal[
        "OK",
        "PREREQUISITE_REQUIRED",
        "BLOCKED",
        "NO_MATCH"
    ]
    lectures: List[Lecture]
    reason: Optional[str] = None
