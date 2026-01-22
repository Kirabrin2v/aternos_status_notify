import os
import time

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder
)

from config import SERVER_HOST, SERVER_PORT, TG_CHAT_ID
from event_bus import event_bus
from handlers.commands import check_server_handler
from handlers.notify import notify_server_on, notify_server_off, notify_server_starting
from minecraft_connector import MinecraftServer


async def send_message(chat_id: int, text: str):
    """
    Отправляет сообщение.

    Функция нужна для отправки сообщений через event_bus из модулей,
    где нет объекта app.
    Args:
        chat_id (int): Telegram ID.
        text (str): Текст сообщения.

    """
    await app.bot.send_message(chat_id, text)

async def post_init(app: "Application"):
    """Инициализирует объекты, которым нужен app"""
    event_bus.subscribe("need_send_message", send_message)
    await server.start_monitor()


if __name__ == "__main__":
    load_dotenv()

    server = MinecraftServer(host=SERVER_HOST, port=SERVER_PORT)

    TOKEN = os.getenv("TG_TOKEN")
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    event_bus.subscribe("server_off", notify_server_off)
    event_bus.subscribe("server_on", notify_server_on)
    event_bus.subscribe("server_starting", notify_server_starting)

    app.add_handler(check_server_handler)

    app.run_polling()
