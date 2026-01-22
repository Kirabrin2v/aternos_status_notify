import time
from typing import Any, Callable

from config import SERVER_HOST, SERVER_PORT, TG_CHAT_ID
from event_bus import event_bus


last_starting_notify_time = 0

def filter_address(host: str, port: int | None) -> Callable[Callable, Callable]:
    """
    Фильтрует не подходящие адреса.

    Предназначен для функций-оповещений. Функция вызовется только в том случае,
    если адрес события равен указанному адресу.

    Args:
        host (str): host (str): Айпи/домен.
        port (int): Порт сервера.    
    """
    def decorator(func) -> Callable[..., Callable]:
        def wrapper(*args, **kwargs) -> Any:
            expected_address = f"{host}:{port}" if port is not None else host
            received_address = args[0]
            if expected_address == received_address:
                return func(*args, **kwargs)
        return wrapper
    return decorator

@filter_address(host=SERVER_HOST, port=SERVER_PORT)
async def notify_server_on(address: str):
    """Оповещает о включении сервера."""
    await event_bus.publish("need_send_message", TG_CHAT_ID, f"✅ Сервер {address} запустился!")

@filter_address(host=SERVER_HOST, port=SERVER_PORT)
async def notify_server_off(address: str):
    """Оповещает о выключении сервера."""
    await event_bus.publish("need_send_message", TG_CHAT_ID, f"❌ Сервер {address} выключился!")

@filter_address(host=SERVER_HOST, port=SERVER_PORT)
async def notify_server_starting(address: str, left_minutes: int):
    """
    Оповещает о подготовке сервера к включению.

    Args:
        address (str): Строка вида host:port или host.
    """
    global last_starting_notify_time

    is_notify_minute = left_minutes % 5 == 0 or left_minutes == 1
    cooldown_passed = time.time() - last_starting_notify_time > 60
    if is_notify_minute and cooldown_passed:
        last_starting_notify_time = time.time()
        if left_minutes % 5 == 0:
            text = f"Сервер {address} включится через {left_minutes} минут!"
        else:
            text = f"До включения сервера {address} осталось менее минуты!"

        await event_bus.publish(
            "need_send_message",
            TG_CHAT_ID,
            answ
        )
