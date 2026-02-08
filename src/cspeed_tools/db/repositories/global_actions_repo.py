from . import BaseRepository

class GlobalActionsRepository(BaseRepository):
    async def add_global_ban(self, user_id: int, reason: str, actor_id: int) -> None:
        await self.db.conn.execute(
            "INSERT OR REPLACE INTO global_bans(user_id, reason, actor_id) VALUES(?,?,?)",
            (user_id, reason, actor_id),
        )
        await self.db.conn.commit()

    async def remove_global_ban(self, user_id: int) -> None:
        await self.db.conn.execute("DELETE FROM global_bans WHERE user_id=?", (user_id,))
        await self.db.conn.commit()

    async def is_globally_banned(self, user_id: int) -> bool:
        cur = await self.db.conn.execute("SELECT 1 FROM global_bans WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row is not None
