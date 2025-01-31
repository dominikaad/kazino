from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pyexpat.errors import messages
from keys.key import kb_start
from loader import router, cursor, con
from aiogram import F


@router.message(Command('start'))
@router.message(F.text == 'Назад')
async def fun_start (message: Message):
    id_user = message.chat.id
    builder = ReplyKeyboardBuilder()
    cursor.execute("SELECT * FROM users WHERE id = (?)",[id_user])
    a = cursor.fetchall()
    if not a:
        cursor.execute(
            "INSERT INTO users (id) VALUES (?)",
            [id_user])
        con.commit()
    for button in kb_start:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text='Йоу бро',
                         reply_markup=builder.as_markup(resize_keyboard=True))

