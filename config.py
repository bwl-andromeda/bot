import os
from pydantic import SecretStr
from pydantic_settings import (
    BaseSettings, SettingsConfigDict
)


class Setting(BaseSettings):
    TOKEN: SecretStr
    DB_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8"
    )


settings = Setting()

