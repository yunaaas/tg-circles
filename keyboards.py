from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



mode_selection = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mode_square = KeyboardButton("Square Mode")
mode_auto = KeyboardButton("Auto Mode")
mode_selection.row(mode_square, mode_auto)