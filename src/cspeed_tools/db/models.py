from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class GlobalBan:
    user_id: int
    reason: str
    actor_id: int
    created_at: datetime
