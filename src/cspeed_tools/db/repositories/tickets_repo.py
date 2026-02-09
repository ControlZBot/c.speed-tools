from . import BaseRepository


class TicketsRepository(BaseRepository):
    async def open_ticket(self, guild_id: int, channel_id: int, created_by: int) -> int:
        cursor = await self.db.conn.execute(
            "INSERT INTO tickets(guild_id, channel_id, created_by) VALUES(?,?,?)",
            (guild_id, channel_id, created_by),
        )
        await self.db.conn.commit()
        return int(cursor.lastrowid)

    async def claim_ticket(self, ticket_id: int, actor_id: int) -> bool:
        cursor = await self.db.conn.execute(
            """
            UPDATE tickets
            SET claimed_by=?, claimed_at=CURRENT_TIMESTAMP
            WHERE id=? AND status='open' AND claimed_by IS NULL
            """,
            (actor_id, ticket_id),
        )
        await self.db.conn.commit()
        return cursor.rowcount == 1

    async def add_message(self, ticket_id: int, author_id: int, content: str) -> None:
        await self.db.conn.execute(
            "INSERT INTO ticket_messages(ticket_id, author_id, content) VALUES(?,?,?)",
            (ticket_id, author_id, content),
        )
        await self.db.conn.commit()

    async def close_ticket(self, ticket_id: int, actor_id: int, transcript_path: str) -> bool:
        cursor = await self.db.conn.execute(
            """
            UPDATE tickets
            SET status='closed', closed_by=?, closed_at=CURRENT_TIMESTAMP, transcript_path=?
            WHERE id=? AND status!='closed'
            """,
            (actor_id, transcript_path, ticket_id),
        )
        await self.db.conn.commit()
        return cursor.rowcount == 1

    async def get_ticket_messages(self, ticket_id: int) -> list[tuple[int, str]]:
        cursor = await self.db.conn.execute(
            "SELECT author_id, content FROM ticket_messages WHERE ticket_id=? ORDER BY id ASC",
            (ticket_id,),
        )
        rows = await cursor.fetchall()
        return [(int(row[0]), str(row[1])) for row in rows]
