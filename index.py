import json

from aiogram import (Bot, Dispatcher)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from routers import router as main_router
from core.config import settings
from upload import check_quotes, upload_quotes

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
dp.include_router(main_router)


async def handler(event, context):
    """
    Entry point
    Точка входа в функцию
    (index.handler)
    """

    # Загрузка цитат, если их нет в базе
    check = await check_quotes()
    if not check:
        await upload_quotes()

    # request_body_dict = json.loads(event['body'])
    request_body_dict = json.loads(event["messages"][0]["details"]["message"]["body"])
    await dp.feed_webhook_update(bot=bot, update=request_body_dict)
    return {'statusCode': 200}
