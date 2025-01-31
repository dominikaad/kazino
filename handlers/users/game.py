from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keys.key import kb_menu, kb_kaz, kb_kub, kb_back
from loader import router
from aiogram import F
import sqlite3
from aiogram import Bot, Dispatcher, Router
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

con = sqlite3.connect('data/data.db', check_same_thread=False)
cursor = con.cursor()
win = 0
fall = 0
res = 0
mon = 0

@router.message(F.text == 'Мои данные')
async def fun_text(message: Message):
    id_user = message.chat.id
    cursor.execute("SELECT money FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    money = a[0][0]
    await message.answer(text=f'Ваш баланс: {money}', reply_markup=types.ReplyKeyboardRemove())

@router.message(F.text == 'Меню')
async def fun_text(message: Message):
    builder = InlineKeyboardBuilder()
    await message.answer(text='Выбери игру, в которую хочешь сыграть', reply_markup=types.ReplyKeyboardRemove())
    for button in kb_menu:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text='Испытай свою удачу',reply_markup=builder.as_markup(resize_keyboard=True))

@router.callback_query(F.data.startswith('kaz'))
async def exit(callback: types.CallbackQuery, bot: Bot):
    global mon
    id_user = callback.message.chat.id
    builder = InlineKeyboardBuilder()
    cursor.execute("SELECT money FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    money = a[0][0]
    mon += money
    await callback.message.answer(text='Ипытай свою удачу!', reply_markup=types.ReplyKeyboardRemove())
    for button in kb_kaz:
        builder.add(button)
    builder.adjust(1)
    await callback.message.answer(text=f'Ваш баланс: {money}\nДелаем ставку?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@router.callback_query(F.data.startswith('exit'))
async def exit(callback: types.CallbackQuery, bot: Bot):
    global fall, win, res, mon
    builder = ReplyKeyboardBuilder()
    for button in kb_back:
        builder.add(button)
    builder.adjust(1)
    await callback.message.answer(text=f'За игру вы выиграли {win} раз\n И проиграли {fall} раз')
    id_user = callback.message.chat.id
    cursor.execute("SELECT money FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    money_user = a[0][0]
    res = mon - money_user
    if res < 0:
        res *= -1
        await callback.message.answer(text=f'За игру вы обрели {res} 🤑', reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text=f'За игру вы потеряли {res} 😢', reply_markup=builder.as_markup(resize_keyboard=True))

@router.callback_query(F.data.startswith('bet'))
async def game(callback: types.CallbackQuery, bot: Bot):
    global fall, win, res
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
            fall += 1
            cursor.execute(
                "update users set money=(?) where id=(?)",
                [money_user, id_user])
            con.commit()
            await callback.message.answer(text='Ты проиграл')
        else:
            money_user += bet
            win += 1
            cursor.execute(
                "update users set money=(?) where id=(?)",
                [money_user, id_user])
            con.commit()
            await callback.message.answer(text=f'Вы выиграли {bet}')
        builder = InlineKeyboardBuilder()
        for button in kb_kaz:
            builder.add(button)
        builder.adjust(1)
        await bot.send_message(text=f'Ваш баланс: {money_user}\nДелаем ставку?',
                               chat_id=id_user,
                               reply_markup=builder.as_markup(resize_keyboard=True))

@router.callback_query(F.data.startswith('kub'))
async def exit(callback: types.CallbackQuery, bot: Bot):
    global mon
    id_user = callback.message.chat.id
    builder = InlineKeyboardBuilder()
    cursor.execute("SELECT money FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    money = a[0][0]
    mon += money
    await callback.message.answer(text='Ипытай свою удачу!', reply_markup=types.ReplyKeyboardRemove())
    for button in kb_kub:
        builder.add(button)
    builder.adjust(1)
    await callback.message.answer(text=f'Ваш баланс: {money}\nДелаем ставку?',
                         reply_markup=builder.as_markup(resize_keyboard=True))

@router.callback_query(F.data.startswith('stav'))
async def game(callback: types.CallbackQuery, bot: Bot):
    global fall, win, res
    stav = int(callback.data.split('_')[1])
    id_user = callback.message.chat.id
    cursor.execute("SELECT money FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    money_user = a[0][0]
    if stav > money_user:
        await callback.answer(text='Недостаточно средств на счету')
    else:
        await callback.message.answer(text='Ваша ставка принята')
        dice_mess = await callback.message.answer_dice(emoji='🎲')
        value_dice = dice_mess.dice.value
        if value_dice <= 3:
            money_user -= stav
            fall += 1
            cursor.execute(
                "update users set money=(?) where id=(?)",
                [money_user, id_user])
            con.commit()
            await callback.message.answer(text='Ты проиграл')
        else:
            money_user += stav
            win += 1
            cursor.execute(
                "update users set money=(?) where id=(?)",
                [money_user, id_user])
            con.commit()
            await callback.message.answer(text=f'Вы выиграли {stav}')
        builder = InlineKeyboardBuilder()
        for button in kb_kub:
            builder.add(button)
        builder.adjust(1)
        await bot.send_message(text=f'Ваш баланс: {money_user}\nДелаем ставку?',
                               chat_id=id_user,
                               reply_markup=builder.as_markup(resize_keyboard=True))