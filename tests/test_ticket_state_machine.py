import pytest

from cspeed_tools.db.engine import Database
from cspeed_tools.db.migrations import run_migrations
from cspeed_tools.db.repositories.tickets_repo import TicketsRepository
from cspeed_tools.services.ticket_service import TicketService


@pytest.mark.asyncio
async def test_ticket_state_machine_claim_and_close(tmp_path) -> None:
    db = Database(f"sqlite+aiosqlite:///{tmp_path}/tickets.db")
    await db.connect()
    await run_migrations(db)
    service = TicketService(TicketsRepository(db))

    ticket_id = await service.open_ticket(1, 2, 3)
    assert await service.claim_ticket(ticket_id, 5)
    assert not await service.claim_ticket(ticket_id, 6)

    await service.append_message(ticket_id, 5, "hello")
    transcript = await service.close_ticket(ticket_id, 5, transcripts_dir=str(tmp_path / "transcripts"))
    assert transcript.endswith(f"ticket-{ticket_id}.txt")

    with pytest.raises(ValueError):
        await service.close_ticket(ticket_id, 5, transcripts_dir=str(tmp_path / "transcripts"))

    await db.close()
