from pydantic import BaseSettings
from pydantic.error_wrappers import ValidationError


class Settings(BaseSettings):
    api_key: str
    api_secret: str
    params_file: str
    base_url: str
    symbol: str = "BTCUSDT"


try:
    settings = Settings(_env_file="./.env", _env_file_encoding="utf-8")
except ValidationError:
    settings = Settings(_env_file="../.env", _env_file_encoding="utf-8")
