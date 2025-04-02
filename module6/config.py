import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalConfig(BaseSettings):
    DATABASE_URL: str = ""
    DB_FORCE_ROLL_BACK: bool = False

    model_config = SettingsConfigDict(env_file="module6/.env", extra="ignore")


class ProdConfig(GlobalConfig):
    pass


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_file="module6/.env.dev", extra="ignore")


class TestConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_file="module6/.env.test", extra="ignore")


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


env_type = os.getenv("ENV_STATE", default="dev")
config = get_config(env_type)
print(env_type)
print(config)
