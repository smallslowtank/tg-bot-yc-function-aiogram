from aiogram import Router, types, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import InputMediaPhoto, URLInputFile

from crud import add_user, last_quote, random_quote, update_user
from filters.chat_types import ChatTypeFilter
from keyboards.inline import get_callback_buttons
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

    # Получить идентификатор пользователя телеграм
    user = callback.from_user
    user_id = user.id

    # Получить последнюю цитату для пользователя
    last_quote_id = await last_quote(user_id)
    if 1 > last_quote_id or last_quote_id > 10:
        # Если такого идентификатора нет в базе, получить цитату и добавить пользователя в базу
        quote_id, quote, author = await random_quote()
        await add_user(user_id, quote_id)
    else:
        # Иначе получить цитату и сравнить с последней
        quote_id, quote, author = await random_quote()
        while last_quote_id == quote_id:
            # Если цитаты совпали, то получить цитату ещё раз
            quote_id, quote, author = await random_quote()
        # Обновить последнюю цитату пользователя в базе
        await update_user(user_id, quote_id)

    # Текст и изображение для ответа
    caption = f"{quote}\n🔖 {author}"
    photo = settings.URL_IMG

    # Отправить (редактировать) сообщение
    await callback.message.edit_media(
        media=InputMediaPhoto(media=URLInputFile(url=photo), caption=caption),
        reply_markup=get_callback_buttons(
            buttons={
                'Ещё цитату? Клац-клац на кнопку! 📝': 'click'
            },
            sizes=(1,)
        )
    )
