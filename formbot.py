import re
from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from logger import logger

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = '7222869117:AAFHMqMZcWBYky4usSp94UihV2CbI1mTVJo'

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Стани для анкети
class ApplicationForm(StatesGroup):
    """
    Стан FSM для збору даних користувача.
    """
    position = State()  # Вибір посади
    full_name = State()  # ПІБ
    birth_date = State()  # Дата народження
    birth_place = State()  # Місце народження
    address_factual = State()  # Адреса фактична
    address_registered = State()  # Адреса реєстрації
    phone_work = State()  # Робочий телефон
    phone_mobile = State()  # Мобільний телефон
    email = State()  # Електронна пошта
    marital_status = State()  # Сімейний стан
    children = State()  # Діти
    education = State()  # Освіта
    work_experience = State()  # Трудова діяльність
    additional_skills = State()  # Додаткові навички
    language_skills = State()  # Знання мов
    pc_skills = State()  # Володіння ПК
    hobbies = State()  # Хобі
    minimum_salary = State()  # Мінімальний рівень зарплати
    preferred_work_time = State()  # Бажаний режим роботи
    work_motivation = State()  # Найбільший стимул в роботі
    personal_qualities = State()  # Особисті якості для роботи
    work_style = State()  # Стиль роботи
    medical_check = State()  # Медичний облік
    court_involvement = State()  # Залучення до суду або слідства
    travel_readiness = State()  # Готовність до відряджень
    driving_experience = State()  # Управління автомобілем (категорії)
    employment_center_status = State()  # Облік у Державному Центрі зайнятості

# Перевірка дати народження у форматі DD.MM.YYYY
def validate_birth_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

# Перевірка коректності email
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Команда /start для початку заповнення анкети
@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started the bot")
    """
        Обробник команди /start. Запускає опитування користувача.

        Args:
            message (Message): Об'єкт повідомлення.
            state (FSMContext): Контекст збереження стану FSM.
        """
    # Запропонуємо вибір позицій через клавіатуру
    builder = ReplyKeyboardBuilder()
    builder.button(text="Продавець-консультант")
    builder.button(text="Менеджер (управитель) в оптовій торгівлі")
    builder.button(text="1С Адміністратор")
    builder.button(text="1С Програміст")
    builder.button(text="Оператор комп'ютерного набору")
    builder.button(text="Бухгалтер первинної документації")
    builder.button(text="Менеджер з адміністративної діяльності")
    builder.button(text="Менеджер з логістики")
    builder.button(text="Провідний логіст")
    builder.button(text="Водій експедитор")
    builder.button(text="Керівник відділу закупівель")
    builder.button(text="Керівник відділу продажу")
    builder.button(text="Охоронець на магазині")
    builder.button(text="Охоронець на складі")
    builder.button(text="Складський працівник")
    builder.adjust(2)

    await message.answer("Яку посаду бажаєте?", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(ApplicationForm.position)

# Обробка вибору посади
@dp.message(ApplicationForm.position)
async def process_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer("Введіть, будь ласка, ваше повне ім'я (ПІБ).")
    await state.set_state(ApplicationForm.full_name)

# Обробка ПІБ
@dp.message(ApplicationForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    """
        Зберігає повне ім'я користувача.

        Args:
            message (Message): Повідомлення з введеним ім'ям.
            state (FSMContext): Контекст FSM.
        """
    await state.update_data(full_name=message.text)
    await message.answer("Введіть дату народження.")
    await state.set_state(ApplicationForm.birth_date)

# Обробка дати народження
@dp.message(ApplicationForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    if not validate_birth_date(message.text):
        await message.answer("Некоректний формат дати. Введіть дату у форматі ДД.ММ.РРРР.")
    else:
        await state.update_data(birth_date=message.text)
        await message.answer("Введіть місце народження.")
        await state.set_state(ApplicationForm.birth_place)

# Обробка місця народження
@dp.message(ApplicationForm.birth_place)
async def process_birth_place(message: Message, state: FSMContext):
    await state.update_data(birth_place=message.text)
    await message.answer("Введіть фактичну адресу проживання.")
    await state.set_state(ApplicationForm.address_factual)

# Обробка фактичної адреси
@dp.message(ApplicationForm.address_factual)
async def process_address_factual(message: Message, state: FSMContext):
    await state.update_data(address_factual=message.text)
    await message.answer("Введіть адресу реєстрації (за паспортом).")
    await state.set_state(ApplicationForm.address_registered)

# Обробка адреси реєстрації
@dp.message(ApplicationForm.address_registered)
async def process_address_registered(message: Message, state: FSMContext):
    await state.update_data(address_registered=message.text)
    await message.answer("Введіть робочий номер телефону.")
    await state.set_state(ApplicationForm.phone_work)

# Обробка робочого телефону
@dp.message(ApplicationForm.phone_work)
async def process_phone_work(message: Message, state: FSMContext):
    await state.update_data(phone_work=message.text)
    await message.answer("Введіть ваш мобільний номер телефону.")
    await state.set_state(ApplicationForm.phone_mobile)

# Обробка мобільного телефону
@dp.message(ApplicationForm.phone_mobile)
async def process_phone_mobile(message: Message, state: FSMContext):
    await state.update_data(phone_mobile=message.text)
    await message.answer("Введіть вашу електронну пошту.")
    await state.set_state(ApplicationForm.email)

# Обробка електронної пошти
@dp.message(ApplicationForm.email)
async def process_email(message: Message, state: FSMContext):
    if not validate_email(message.text):
        await message.answer("Некоректна електронна адреса. Введіть дійсну адресу.")
    else:
        await state.update_data(email=message.text)
        await message.answer("Вкажіть ваш сімейний стан (одружений/неодружений).")
        await state.set_state(ApplicationForm.marital_status)

# Обробка сімейного стану
@dp.message(ApplicationForm.marital_status)
async def process_marital_status(message: Message, state: FSMContext):
    await state.update_data(marital_status=message.text)
    await message.answer("Вкажіть, чи є у вас діти та їх вік.")
    await state.set_state(ApplicationForm.children)

# Обробка інформації про дітей
@dp.message(ApplicationForm.children)
async def process_children(message: Message, state: FSMContext):
    await state.update_data(children=message.text)
    await message.answer("Вкажіть вашу освіту (назва закладу, спеціальність, рік випуску).")
    await state.set_state(ApplicationForm.education)

# Обробка освіти
@dp.message(ApplicationForm.education)
async def process_education(message: Message, state: FSMContext):
    await state.update_data(education=message.text)
    await message.answer("Опишіть вашу трудову діяльність (місце роботи, посада, обов'язки).")
    await state.set_state(ApplicationForm.work_experience)

# Обробка трудової діяльності
@dp.message(ApplicationForm.work_experience)
async def process_work_experience(message: Message, state: FSMContext):
    await state.update_data(work_experience=message.text)
    await message.answer("Вкажіть ваші додаткові навички (курси, тренінги тощо).")
    await state.set_state(ApplicationForm.additional_skills)

# Обробка додаткових навичок
@dp.message(ApplicationForm.additional_skills)
async def process_additional_skills(message: Message, state: FSMContext):
    await state.update_data(additional_skills=message.text)
    await message.answer("Якими мовами ви володієте та на якому рівні?")
    await state.set_state(ApplicationForm.language_skills)

# Обробка знання мов
@dp.message(ApplicationForm.language_skills)
async def process_language_skills(message: Message, state: FSMContext):
    await state.update_data(language_skills=message.text)
    await message.answer("Оцініть ваш рівень володіння ПК.")
    await state.set_state(ApplicationForm.pc_skills)

# Обробка рівня володіння ПК
@dp.message(ApplicationForm.pc_skills)
async def process_pc_skills(message: Message, state: FSMContext):
    await state.update_data(pc_skills=message.text)
    await message.answer("Вкажіть ваші хобі або захоплення.")
    await state.set_state(ApplicationForm.hobbies)

# Обробка хобі
@dp.message(ApplicationForm.hobbies)
async def process_hobbies(message: Message, state: FSMContext):
    await state.update_data(hobbies=message.text)
    await message.answer("Який мінімальний рівень зарплати ви розраховуєте отримувати?")
    await state.set_state(ApplicationForm.minimum_salary)

# Обробка мінімальної зарплати
@dp.message(ApplicationForm.minimum_salary)
async def process_minimum_salary(message: Message, state: FSMContext):
    await state.update_data(minimum_salary=message.text)
    await message.answer("Вкажіть бажаний режим роботи (денний/нічний/змінний).")
    await state.set_state(ApplicationForm.preferred_work_time)

# Обробка бажаного режиму роботи
@dp.message(ApplicationForm.preferred_work_time)
async def process_preferred_work_time(message: Message, state: FSMContext):
    await state.update_data(preferred_work_time=message.text)
    await message.answer("Найбільший стимул в роботі.")
    await state.set_state(ApplicationForm.work_motivation)

# Обробка стимулу в роботі
@dp.message(ApplicationForm.work_motivation)
async def process_work_motivation(message: Message, state: FSMContext):
    await state.update_data(work_motivation=message.text)
    await message.answer("Які ваші особисті (ділові, професійні) якості будуть корисні в роботі?")
    await state.set_state(ApplicationForm.personal_qualities)

# Обробка особистих якостей
@dp.message(ApplicationForm.personal_qualities)
async def process_personal_qualities(message: Message, state: FSMContext):
    await state.update_data(personal_qualities=message.text)
    await message.answer("Який стиль роботи вам ближче: індивідуальний чи колективний?")
    await state.set_state(ApplicationForm.work_style)

# Обробка стилю роботи
@dp.message(ApplicationForm.work_style)
async def process_work_style(message: Message, state: FSMContext):
    await state.update_data(work_style=message.text)
    await message.answer("Чи перебуваєте ви на медичному обліку?")
    await state.set_state(ApplicationForm.medical_check)

# Обробка інформації про медичний облік
@dp.message(ApplicationForm.medical_check)
async def process_medical_check(message: Message, state: FSMContext):
    await state.update_data(medical_check=message.text)
    await message.answer("Чи були ви залучені до суду або слідства?")
    await state.set_state(ApplicationForm.court_involvement)

# Обробка залучення до суду або слідства
@dp.message(ApplicationForm.court_involvement)
async def process_court_involvement(message: Message, state: FSMContext):
    await state.update_data(court_involvement=message.text)
    await message.answer("Чи готові ви до відряджень?")
    await state.set_state(ApplicationForm.travel_readiness)

# Обробка готовності до відряджень
@dp.message(ApplicationForm.travel_readiness)
async def process_travel_readiness(message: Message, state: FSMContext):
    await state.update_data(travel_readiness=message.text)
    await message.answer("Чи маєте ви водійське посвідчення? Якщо так, вкажіть категорію.")
    await state.set_state(ApplicationForm.driving_experience)

# Обробка водійського посвідчення
@dp.message(ApplicationForm.driving_experience)
async def process_driving_experience(message: Message, state: FSMContext):
    await state.update_data(driving_experience=message.text)
    await message.answer("Чи перебуваєте Ви на обліку в Державному Центрі зайнятості населення?")
    await state.set_state(ApplicationForm.employment_center_status)

# Обробка статусу в Державному Центрі зайнятості
@dp.message(ApplicationForm.employment_center_status)
async def process_employment_center_status(message: Message, state: FSMContext):
    await state.update_data(employment_center_status=message.text)

    # Отримуємо всі зібрані дані анкети
    user_data = await state.get_data()

    # Відправка анкети в канал або чат
    chat_id = '-4577772999'  #ID чату або каналу
    await bot.send_message(
        chat_id,
        f"Нова анкета:\n\n"
        f"Позиція: {user_data['position']}\n"
        f"Ім'я: {user_data['full_name']}\n"
        f"Дата народження: {user_data['birth_date']}\n"
        f"Місце народження: {user_data['birth_place']}\n"
        f"Фактична адреса: {user_data['address_factual']}\n"
        f"Адреса реєстрації: {user_data['address_registered']}\n"
        f"Робочий телефон: {user_data['phone_work']}\n"
        f"Мобільний телефон: {user_data['phone_mobile']}\n"
        f"Електронна пошта: {user_data['email']}\n"
        f"Сімейний стан: {user_data['marital_status']}\n"
        f"Діти: {user_data['children']}\n"
        f"Освіта: {user_data['education']}\n"
        f"Трудова діяльність: {user_data['work_experience']}\n"
        f"Додаткові навички: {user_data['additional_skills']}\n"
        f"Знання мов: {user_data['language_skills']}\n"
        f"Володіння ПК: {user_data['pc_skills']}\n"
        f"Хобі: {user_data['hobbies']}\n"
        f"Мінімальна зарплата: {user_data['minimum_salary']}\n"
        f"Бажаний режим роботи: {user_data['preferred_work_time']}\n"
        f"Найбільший стимул в роботі: {user_data['work_motivation']}\n"
        f"Корисні якості: {user_data['personal_qualities']}\n"
        f"Стиль роботи: {user_data['work_style']}\n"
        f"Медичний облік: {user_data['medical_check']}\n"
        f"Залучення до суду або слідства: {user_data['court_involvement']}\n"
        f"Готовність до відряджень: {user_data['travel_readiness']}\n"
        f"Категорії водійського посвідчення: {user_data['driving_experience']}\n"
        f"Статус у Центрі зайнятості: {user_data['employment_center_status']}"
    )

    # Підтвердження заповнення анкети
    await message.answer(
        f"Дякую за заповнення анкети! Ось ваша анкета:\n\n"
        f"Позиція: {user_data['position']}\n"
        f"Ім'я: {user_data['full_name']}\n"
        f"Дата народження: {user_data['birth_date']}\n"
        f"Місце народження: {user_data['birth_place']}\n"
        f"Фактична адреса: {user_data['address_factual']}\n"
        f"Адреса реєстрації: {user_data['address_registered']}\n"
        f"Робочий телефон: {user_data['phone_work']}\n"
        f"Мобільний телефон: {user_data['phone_mobile']}\n"
        f"Електронна пошта: {user_data['email']}\n"
        f"Сімейний стан: {user_data['marital_status']}\n"
        f"Діти: {user_data['children']}\n"
        f"Освіта: {user_data['education']}\n"
        f"Трудова діяльність: {user_data['work_experience']}\n"
        f"Додаткові навички: {user_data['additional_skills']}\n"
        f"Знання мов: {user_data['language_skills']}\n"
        f"Володіння ПК: {user_data['pc_skills']}\n"
        f"Хобі: {user_data['hobbies']}\n"
        f"Мінімальна зарплата: {user_data['minimum_salary']}\n"
        f"Бажаний режим роботи: {user_data['preferred_work_time']}\n"
        f"Найбільший стимул в роботі: {user_data['work_motivation']}\n"
        f"Корисні якості: {user_data['personal_qualities']}\n"
        f"Стиль роботи: {user_data['work_style']}\n"
        f"Медичний облік: {user_data['medical_check']}\n"
        f"Залучення до суду або слідства: {user_data['court_involvement']}\n"
        f"Готовність до відряджень: {user_data['travel_readiness']}\n"
        f"Категорії водійського посвідчення: {user_data['driving_experience']}\n"
        f"Статус у Центрі зайнятості: {user_data['employment_center_status']}",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Скидання стану після завершення анкети
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
