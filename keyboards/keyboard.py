from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


html_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='TXT в PDF')],[KeyboardButton(text='DOCX в PDF')],[KeyboardButton(text='ODT в PDF')],[KeyboardButton(text='Изображение в PDF')]],
        resize_keyboard=True
    )
