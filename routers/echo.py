from aiogram import Router, types

from filters.chat_types import ChatTypeFilter

router = Router(name=__name__)
router.message.filter(ChatTypeFilter(["private"]))


@router.message()
async def handle_echo(message: types.Message):
    """
    Обработка сообщений из чата (эхо)
    """
    text = "Нужно подумать...👀"
    await message.answer(
        text=text
    )
    text = "В смысле?\nНипанятна!\nЖми /start"
    await message.answer(
        reply_to_message_id=message.message_id,
        text=text
    )
