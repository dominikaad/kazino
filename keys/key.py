from aiogram import types

kb_start = [
    types.KeyboardButton(text='Мои данные'),
    types.KeyboardButton(text='Меню')
]

kb_back = [
    types.KeyboardButton(text='Назад')
]

kb_kaz = [
    types.InlineKeyboardButton(text='ставка 100', callback_data='bet_100'),
    types.InlineKeyboardButton(text='ставка 200', callback_data='bet_200'),
    types.InlineKeyboardButton(text='ставка 300', callback_data='bet_300'),
    types.InlineKeyboardButton(text='ставка 400', callback_data='bet_400'),
    types.InlineKeyboardButton(text='ставка 500', callback_data='bet_500'),
    types.InlineKeyboardButton(text='Назад', callback_data='exit_res')
]

kb_menu = [
    types.InlineKeyboardButton(text='kazino', callback_data='kaz'),
    types.InlineKeyboardButton(text='kubik', callback_data='kub')]

kb_kub = [
    types.InlineKeyboardButton(text='ставка 100', callback_data='stav_100'),
    types.InlineKeyboardButton(text='ставка 200', callback_data='stav_200'),
    types.InlineKeyboardButton(text='ставка 300', callback_data='stav_300'),
    types.InlineKeyboardButton(text='ставка 400', callback_data='stav_400'),
    types.InlineKeyboardButton(text='ставка 500', callback_data='stav_500'),
    types.InlineKeyboardButton(text='Назад', callback_data='exit_res')
]