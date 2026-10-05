import os
import re
from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from managers.service_manager import ServiceManager


# Налаштування
load_dotenv()

BOT_TOKEN = os.getenv("BEAUTY_BOT_TOKEN")

if BOT_TOKEN:
    print(f"🔑 BOT_TOKEN: {BOT_TOKEN[:10]}...")
else:
    print("❌ BEAUTY_BOT_TOKEN не знайдено")


# ServiceManager
print("🔧 Ініціалізація ServiceManager...")

service_manager = ServiceManager()

print("✅ ServiceManager ініціалізовано")


# Розбір даних клієнта
def parse_client_message(text: str):
    """
    Розбирає повідомлення:
    Ім'я Телефон Email
    Ім'я може складатися з будь-якої
    кількості слів.
    """
    text = text.strip()

    if not text:
        raise ValueError(
            "Повідомлення порожнє."
        )

    # Шукаємо email
    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if not email_match:
        raise ValueError(
            "Не вдалося знайти email.\n\n"
            "Приклад:\n"
            "Олена Коваленко "
            "0671234567 "
            "olena@example.com"
        )

    email = email_match.group(0)

    before_email = text[:email_match.start()].strip()
    after_email = text[email_match.end():].strip()

    if after_email:
        raise ValueError(
            "Після email не повинно бути додаткового тексту."
        )

    # Шукаємо телефон
    phone_candidates = re.findall(
        r"(?:\+?\d[\d\s().-]{7,}\d)",
        before_email
    )

    if not phone_candidates:
        raise ValueError(
            "Не вдалося знайти номер телефону.\n\n"
            "Приклади:\n"
            "0671234567\n"
            "067 123 45 67\n"
            "+380671234567\n"
            "+380 67 123 45 67"
        )

    # Останній кандидат вважаємо телефоном.
    phone = phone_candidates[-1]

    # Все перед телефоном = ім'я
    phone_position = before_email.rfind(phone)

    name = before_email[:phone_position].strip()

    if not name:
        raise ValueError(
            "Не вдалося визначити ім'я клієнта."
        )

    return name, phone, email


# START
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Команда /start."""

    print(
        f"📨 Отримано /start від користувача: "
        f"{update.effective_user.id}"
    )

    keyboard = [
        [KeyboardButton("➕ Додати клієнта")],
        [KeyboardButton("👥 Клієнти")],
        [KeyboardButton("🛠️ Послуги")],
        [KeyboardButton("📋 Замовлення")],
        [KeyboardButton("❓ Допомога")]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "👋 Вітаю в Beauty Clinic Bot!\n\n"
        "Оберіть потрібну дію в меню нижче.\n\n"
        "Доступні команди:\n"
        "/start - початок роботи\n"
        "/add_client - додати клієнта\n"
        "/list_clients - клієнти\n"
        "/list_services - послуги\n"
        "/list_orders - замовлення\n"
        "/help - допомога",
        reply_markup=reply_markup
    )


# HELP
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Команда /help."""

    await update.message.reply_text(
        "🆘 Допомога\n\n"
        "Доступні команди:\n"
        "/start - початок роботи\n"
        "/add_client - додати клієнта\n"
        "/list_clients - клієнти\n"
        "/list_services - послуги\n"
        "/list_orders - замовлення\n"
        "/help - ця довідка\n\n"
        "Для додавання клієнта введіть:\n"
        "Ім'я Телефон Email\n\n"
        "Наприклад:\n"
        "Олена Петрівна Коваленко "
        "067 123 45 67 "
        "olena@example.com"
    )


# ДОДАВАННЯ КЛІЄНТА
async def add_client(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Показує інструкцію для додавання клієнта."""

    await update.message.reply_text(
        "📝 Додавання клієнта\n\n"
        "Введіть одним повідомленням:\n"
        "Ім'я Телефон Email\n\n"
        "Ім'я може складатися з кількох слів.\n\n"
        "Наприклад:\n"
        "Олена Коваленко "
        "0671234567 "
        "olena@example.com\n\n"
        "Або:\n"
        "Олена Петрівна Коваленко "
        "+380 67 123 45 67 "
        "olena@example.com\n\n"
        "Телефон можна вводити з +380, 380, 80 "
        "або 0, з пробілами чи дефісами."
    )


# ОБРОБКА
async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Обробляє введені користувачем дані."""

    text = update.message.text.strip()

    try:
        name, phone, email = parse_client_message(text)

    except ValueError as e:
        await update.message.reply_text(
            f"❌ {e}\n\n"
            "Будь ласка, спробуйте ще раз."
        )
        return

    try:
        client_id = service_manager.add_client_with_params(
            name=name,
            phone=phone,
            email=email
        )

        # Останній доданий клієнт
        new_client = service_manager.clients[-1]

        await update.message.reply_text(
            "✅ Клієнта додано успішно!\n\n"
            f"👤 Ім'я: {new_client.name}\n"
            f"📱 Телефон: {new_client.phone}\n"
            f"📧 Email: {new_client.email}\n"
            f"🆔 ID: {client_id}"
        )

    except ValueError as e:
        await update.message.reply_text(
            "❌ Не вдалося додати клієнта.\n\n"
            f"{e}"
        )

    except Exception as e:
        print(
            f"❌ Непередбачена помилка: {e}"
        )

        await update.message.reply_text(
            "❌ Сталася помилка під час "
            "додавання клієнта.\n"
            "Спробуйте ще раз."
        )


# КЛІЄНТИ
async def list_clients(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Показує список клієнтів."""

    clients = service_manager.clients

    if len(clients) == 0:
        await update.message.reply_text(
            "📭 Клієнтів ще немає."
        )
        return

    message = "👥 Список клієнтів:\n\n"

    for i, client in enumerate(clients, 1):
        message += (
            f"{i}. 🆔 ID: {client.id}\n"
            f"👤 {client.name}\n"
            f"📱 {client.phone}\n"
            f"📧 {client.email}\n\n"
        )

    await update.message.reply_text(message)


# ПОСЛУГИ
async def list_services(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Показує список послуг."""

    services = service_manager.services

    if len(services) == 0:
        await update.message.reply_text(
            "🛠️ Послуг ще немає."
        )
        return

    message = "🛠️ Список послуг:\n\n"

    for i, service in enumerate(services, 1):
        message += (
            f"{i}. {service.name}\n"
            f"💰 Ціна: {service.price}\n"
            f"⏱️ Тривалість: "
            f"{service.duration} хв.\n\n"
        )

    await update.message.reply_text(message)


# ЗАМОВЛЕННЯ
async def list_orders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Показує список замовлень."""

    orders = service_manager.orders

    if len(orders) == 0:
        await update.message.reply_text(
            "📋 Замовлень ще немає."
        )
        return

    status_map = {
        "Created": "Створено",
        "Scheduled": "Заплановано",
        "In Progress": "В процесі",
        "Done": "Виконано",
        "Completed": "Завершено",
        "Cancelled": "Скасовано",
        "Unknown": "Невідомо"
    }

    message = "📋 Список замовлень:\n\n"

    for i, order in enumerate(orders, 1):
        translated_status = status_map.get(
            order.status,
            order.status
        )

        message += (
            f"{i}. 🆔 ID: {order.id}\n"
            f"🛠️ Послуга: {order.service_name}\n"
            f"📌 Статус: {translated_status}\n"
            f"💰 Ціна: {order.total_price}\n\n"
        )

    await update.message.reply_text(message)


# КНОПКИ МЕНЮ
async def button_add_client(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await add_client(update, context)


async def button_clients(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await list_clients(update, context)


async def button_services(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await list_services(update, context)


async def button_orders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await list_orders(update, context)


async def button_help(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await help_command(update, context)


# MAIN
def main():
    """Запуск бота."""

    if not BOT_TOKEN:
        print(
            "❌ BEAUTY_BOT_TOKEN не знайдено "
            "в .env файлі"
        )
        return

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Команди
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("add_client", add_client)
    )

    application.add_handler(
        CommandHandler("list_clients", list_clients)
    )

    application.add_handler(
        CommandHandler("list_services", list_services)
    )

    application.add_handler(
        CommandHandler("list_orders", list_orders)
    )

    # Кнопки нижнього меню
    application.add_handler(
        MessageHandler(
            filters.Regex("^➕ Додати клієнта$"),
            button_add_client
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^👥 Клієнти$"),
            button_clients
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^🛠️ Послуги$"),
            button_services
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^📋 Замовлення$"),
            button_orders
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^❓ Допомога$"),
            button_help
        )
    )

    # Інші текстові повідомлення
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    print("🤖 Beauty Clinic Bot запущено!")

    application.run_polling()


if __name__ == "__main__":
    main()
