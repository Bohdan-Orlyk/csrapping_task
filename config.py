from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

env_file = find_dotenv()


class DbConfig(BaseSettings):
    user: str
    password: str
    database: str
    host: str
    port: str

    model_config = SettingsConfigDict(env_file=env_file)


db_config = DbConfig()