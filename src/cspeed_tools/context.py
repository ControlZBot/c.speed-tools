from dataclasses import dataclass

@dataclass(slots=True)
class RequestContext:
    guild_id: int | None
    actor_id: int
    reason: str
