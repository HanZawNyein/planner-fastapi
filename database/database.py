from pydantic import BaseSettings, BaseModel
from typing import Optional, List


class Settings(BaseSettings):
    SECRET_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
