from pathlib import Path
from .engine import Database

async def run_migrations(db: Database) -> None:
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    await db.conn.executescript(schema)
    await db.conn.commit()
