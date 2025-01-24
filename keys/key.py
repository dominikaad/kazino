from aiogram import types

kb_start = [
    types.KeyboardButton(text='Играем'),
    types.KeyboardButton(text='Меню')
]

kb_game = [
    types.InlineKeyboardButton(text='ставка 100', callback_data='bet_100'),
    types.InlineKeyboardButton(text='ставка 200', callback_data='bet_200'),
    types.InlineKeyboardButton(text='ставка 300', callback_data='bet_300'),
    types.InlineKeyboardButton(text='ставка 400', callback_data='bet_400'),
    types.InlineKeyboardButton(text='ставка 500', callback_data='bet_500')
]