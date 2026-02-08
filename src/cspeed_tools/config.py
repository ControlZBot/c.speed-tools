from pydantic_settings import BaseSettings, SettingsConfigDict
from .constants import OWNER_DEFAULT_ID

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    bot_token: str
    database_url: str
    dev_guild_id: int | None = None
    owner_user_id: int = OWNER_DEFAULT_ID
    rss_feed_url: str | None = None
    webhook_secret: str | None = None
