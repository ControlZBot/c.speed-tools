from pathlib import Path
from cspeed_tools.db.repositories.tickets_repo import TicketsRepository


class TicketService:
    def __init__(self, repo: TicketsRepository):
        self.repo = repo

    async def open_ticket(self, guild_id: int, channel_id: int, actor_id: int) -> int:
        return await self.repo.open_ticket(guild_id, channel_id, actor_id)

    async def claim_ticket(self, ticket_id: int, actor_id: int) -> bool:
        return await self.repo.claim_ticket(ticket_id, actor_id)

    async def append_message(self, ticket_id: int, author_id: int, content: str) -> None:
        clean = content.strip()
        if not clean:
            return
        await self.repo.add_message(ticket_id, author_id, clean)

    async def close_ticket(self, ticket_id: int, actor_id: int, transcripts_dir: str = "transcripts") -> str:
        messages = await self.repo.get_ticket_messages(ticket_id)
        Path(transcripts_dir).mkdir(parents=True, exist_ok=True)
        transcript_path = Path(transcripts_dir) / f"ticket-{ticket_id}.txt"
        transcript_path.write_text(
            "\n".join(f"{author_id}: {content}" for author_id, content in messages),
            encoding="utf-8",
        )
        closed = await self.repo.close_ticket(ticket_id, actor_id, str(transcript_path))
        if not closed:
            raise ValueError("Ticket already closed or not found")
        return str(transcript_path)
