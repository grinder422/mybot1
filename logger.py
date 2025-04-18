import logging

# Налаштування базового логера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    filemode='a'
)

# Створюємо логер
logger = logging.getLogger("weather_bot")
