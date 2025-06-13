from aiogram import Router, types, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import InputMediaPhoto, URLInputFile

from filters.chat_types import ChatTypeFilter
from keyboards.inline import get_callback_buttons
from queries.read import random_quote
from core.config import settings

router = Router(name=__name__)
router.message.filter(ChatTypeFilter(["private"]))


@router.message(or_f(CommandStart(), F.text.lower() == "start", F.text.lower() == 'старт'))
async def start_command(message: types.Message):
    """
    Команда "старт"
    """
    photo = settings.URL_IMG
    await message.answer_photo(
        photo=URLInputFile(url=photo),
        caption="Нажми на кнопку - получишь результат! 📝",
        reply_markup=get_callback_buttons(
            buttons={
                'Нажми меня!': 'click'
            },
            sizes=(1,)
        )
    )


@router.callback_query(F.data == 'click')
async def start_menu(callback: types.CallbackQuery):
    """
    Коллбек "click"
    """
    quote, author = await random_quote()
    caption = f"{quote}\n🔖 {author}"
    photo = settings.URL_IMG

    await callback.message.edit_media(
        media=InputMediaPhoto(media=URLInputFile(url=photo), caption=caption),
        reply_markup=get_callback_buttons(
            buttons={
                'Ещё цитату? Клац-клац на кнопку! 📝': 'click'
            },
            sizes=(1,)
        )
    )
