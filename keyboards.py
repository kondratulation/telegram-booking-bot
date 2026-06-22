from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Записаться")],
        [KeyboardButton(text="📊 Админ панель")]
    ],
    resize_keyboard=True
)


admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Все заявки")],
        [KeyboardButton(text="🗑 Удалить последнюю")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)