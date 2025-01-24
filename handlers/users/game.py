from aiogram.types import Message, ReplyKeyboardRemove
from keys.key import kb_game
from loader import router
from aiogram import F
import sqlite3
from aiogram import Bot, Dispatcher, Router
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

con = sqlite3.connect('data/data.db', check_same_thread=False)
cursor = con.cursor()

@router.message(F.text == 'Играем')
async def fun_text(message: Message):
    id_user = message.chat.id
    builder = InlineKeyboardBuilder()
    cursor.execute("SELECT money FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    money = a[0][0]
    await message.answer(text='Ипытай свою удачу!', reply_markup=types.ReplyKeyboardRemove())
    for button in kb_game:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text=f'Ваш баланс: {money}\nДелаем ставку?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@router.callback_query(F.data.startswith('bet'))
async def game(callback: types.CallbackQuery, bot: Bot):
    bet = int(callback.data.split('_')[1])
    id_user = callback.message.chat.id
    cursor.execute("SELECT money FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    money_user = a[0][0]
    if bet > money_user:
        await callback.answer(text='Недостаточно средств на счету')
    else:
        await callback.message.answer(text='Ваша ставка принята')
        dice_mess = await callback.message.answer_dice(emoji='🎰')
        value_dice = dice_mess.dice.value
        if value_dice < 32:
            money_user -= bet
            cursor.execute(
                "update users set money=(?) where id=(?)",
                [money_user, id_user])
            con.commit()
            await callback.message.answer(text='Ты проиграл')
        else:
            money_user += bet
            cursor.execute(
                "update users set money=(?) where id=(?)",
                [money_user, id_user])
            con.commit()
            await callback.message.answer(text=f'Вы выиграли {bet}')
        builder = InlineKeyboardBuilder()
        for button in kb_game:
            builder.add(button)
        builder.adjust(1)
        await bot.send_message(text=f'Ваш баланс: {money_user}\nДелаем ставку?',
                               chat_id=id_user,
                               reply_markup=builder.as_markup(resize_keyboard=True))