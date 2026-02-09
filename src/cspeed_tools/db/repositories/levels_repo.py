from . import BaseRepository


class LevelsRepository(BaseRepository):
    async def add_xp(self, guild_id: int, user_id: int, amount: int, event_ts: float) -> int:
        await self.db.conn.execute(
            """
            INSERT INTO level_xp(guild_id, user_id, xp, last_award_ts)
            VALUES(?,?,?,?)
            ON CONFLICT(guild_id, user_id)
            DO UPDATE SET xp = xp + excluded.xp, last_award_ts = excluded.last_award_ts
            """,
            (guild_id, user_id, amount, event_ts),
        )
        await self.db.conn.commit()
        cursor = await self.db.conn.execute(
            "SELECT xp FROM level_xp WHERE guild_id=? AND user_id=?",
            (guild_id, user_id),
        )
        row = await cursor.fetchone()
        return int(row[0])

    async def get_last_award_ts(self, guild_id: int, user_id: int) -> float:
        cursor = await self.db.conn.execute(
            "SELECT last_award_ts FROM level_xp WHERE guild_id=? AND user_id=?",
            (guild_id, user_id),
        )
        row = await cursor.fetchone()
        return float(row[0]) if row else 0.0

    async def get_xp(self, guild_id: int, user_id: int) -> int:
        cursor = await self.db.conn.execute(
            "SELECT xp FROM level_xp WHERE guild_id=? AND user_id=?",
            (guild_id, user_id),
        )
        row = await cursor.fetchone()
        return int(row[0]) if row else 0
