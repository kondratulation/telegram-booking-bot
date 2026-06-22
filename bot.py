import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import main_keyboard
from states import BookingForm
from database import save_booking, create_database, get_bookings
from config import BOT_TOKEN, ADMIN_ID
from keyboards import main_keyboard, admin_keyboard
from database import save_booking, create_database, get_bookings, delete_last_booking


bot = Bot(token=BOT_TOKEN)

from aiogram.fsm.storage.memory import MemoryStorage

dp = Dispatcher(storage=MemoryStorage())

@dp.message(lambda message: message.text == "Мои данные")
async def my_data(message: Message):

    bookings = get_bookings()

    user_id = str(message.from_user.id)

    user_bookings = []

    for b in bookings:
        if b[0] == user_id:
            user_bookings.append(b)

    if not user_bookings:
        await message.answer("У вас пока нет заявок.")
        return

    text = "Ваши заявки:\n\n"

    for user_id, name, phone in user_bookings:
        text += f"{name} — {phone}\n"

    await message.answer(text)

@dp.message(lambda message: message.text == "/start")
async def start(message: Message):

    await message.answer(
        "Привет! Я бот записи клиентов.",
        reply_markup=main_keyboard
    )


@dp.message(lambda message: message.text == "📌 Записаться")
async def booking_start(
        message: Message,
        state: FSMContext
):

    await message.answer(
        "Введите ваше имя:"
    )

    await state.set_state(
        BookingForm.name
    )


@dp.message(BookingForm.name)
async def get_name(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        name=message.text
    )

    await message.answer(
        "Введите ваш номер телефона:"
    )

    await state.set_state(
        BookingForm.phone
    )


@dp.message(BookingForm.phone)
async def get_phone(
        message: Message,
        state: FSMContext
):

    data = await state.get_data()

    name = data["name"]
    phone = message.text

    save_booking(
        str(message.from_user.id),
        name,
        phone
    )

    await message.answer(
        f"Спасибо, {name}! Ваша заявка принята.\n"
        f"Мы скоро с вами свяжемся."
    )


    await state.clear()


@dp.message(lambda message: message.text == "/bookings")
async def show_bookings(message: Message):

    bookings = get_bookings()


    if not bookings:

        await message.answer(
            "Заявок пока нет."
        )

        return


    text = "Список заявок:\n\n"

    for booking in bookings:
        user_id, name, phone = booking

        text += f"{name} — {phone}\n"


    await message.answer(text)

@dp.message(lambda message: message.text == "Сброс")
async def reset(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "Диалог сброшен. Нажмите 'Записаться' для новой заявки."
    )


async def main():

    create_database()

    await dp.start_polling(bot)

@dp.message(lambda message: message.text == "📊 Админ панель")
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        await message.answer("Нет доступа ❌")
        return

    await message.answer(
        "Админ-панель:",
        reply_markup=admin_keyboard
    )

@dp.message(lambda message: message.text == "📋 Все заявки")
async def all_bookings(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    bookings = get_bookings()

    if not bookings:
        await message.answer("Заявок нет")
        return

    text = "📋 Все заявки:\n\n"

    for user_id, name, phone in bookings:
        text += f"{name} — {phone}\n"

    await message.answer(text)


@dp.message(lambda message: message.text == "🗑 Удалить последнюю")
async def remove_last(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    delete_last_booking()

    await message.answer("Последняя заявка удалена ✅")

@dp.message(lambda message: message.text == "🔙 Назад")
async def back(message: Message):

    await message.answer(
        "Главное меню",
        reply_markup=main_keyboard
    )


if __name__ == "__main__":

    asyncio.run(main())

