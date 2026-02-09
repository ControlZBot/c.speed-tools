from . import BaseRepository


class ModerationRepository(BaseRepository):
    async def create_case(
        self,
        guild_id: int,
        actor_id: int,
        target_id: int,
        action: str,
        reason: str,
    ) -> int:
        cursor = await self.db.conn.execute(
            "INSERT INTO cases(guild_id, actor_id, target_id, action, reason) VALUES(?,?,?,?,?)",
            (guild_id, actor_id, target_id, action, reason),
        )
        await self.db.conn.commit()
        return int(cursor.lastrowid)

    async def get_case(self, case_id: int) -> tuple[int, int, int, str, str] | None:
        cursor = await self.db.conn.execute(
            "SELECT guild_id, actor_id, target_id, action, reason FROM cases WHERE id=?",
            (case_id,),
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        return (int(row[0]), int(row[1]), int(row[2]), str(row[3]), str(row[4]))
