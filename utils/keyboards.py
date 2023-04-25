from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)

wallet_reply_markup = InlineKeyboardMarkup()
wallet_reply_markup.add(InlineKeyboardButton(text='Пополнить 💸',
                                             callback_data='replenish'))

replenish_reply_markup = InlineKeyboardMarkup()
replenish_reply_markup.add(InlineKeyboardButton(text='Проверить оплату 💸',
                                             callback_data='check_payment'))

cancel_reply_markup = InlineKeyboardMarkup()
cancel_reply_markup.add(InlineKeyboardButton(text='⏪ Отмена',
                                             callback_data='cancel'))
