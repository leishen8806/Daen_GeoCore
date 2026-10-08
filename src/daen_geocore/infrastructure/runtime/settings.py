from pydantic_settings import BaseSettings, SettingsConfigDict


class RuntimeSettings(BaseSettings):
    """Minimal infrastructure settings for the implementation shell."""

    environment: str = "local"
    log_level: str = "INFO"
    database_url: str = ""

    model_config = SettingsConfigDict(env_prefix="DAEN_", extra="ignore")
