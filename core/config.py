import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # токен бота
    BOT_TOKEN: str = os.environ['BOT_TOKEN']

    # url баннера
    URL_IMG: str = os.environ['URL_IMG']

    # настройки подключения к БД
    YDB_CS: str = os.environ['YDB_CS']


settings = Settings()
