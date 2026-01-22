import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import SERVER_HOST, SERVER_PORT
from logging_config import setup_logging
from minecraft_connector import MinecraftServer


setup_logging()
logger = logging.getLogger(__name__)


def format_server_info(
	host: str,
	is_online: bool,
	port: int | None = None,
	motd: str | None = None,
	players: list[str] = [],
	max_online: int = 20
) -> str:
	"""
	Приводит данные к user-friendly формату.

	Args:
		host (str): Айпи/домен.
		is_online (bool)
		port (int): Порт сервера.
		motd (str): Краткое описание сервера.
		players (list[str]): Список ников.
		max_online (int): Максимальный допустимый онлайн.

	Returns:
		str
	"""
	address = f"{host}:{port}" if port is not None else host
	status_text = "✅ Online" if is_online else "❌ Offline"
	
	text = f"Информация об {address}:\n{status_text}\n"
	
	if motd is not None:
		text += f'"{motd}"\n'
	
	text += f"Игроков: {len(players)}/{max_online}\n"
	for nick in players:
		text += f"◆ {nick}\n"

	return text

def parse_host_and_port(args: list[str]) -> tuple[str | None, int | None]:
	"""
	Парсит из переданных аргументов хост и порт.

	Args:
		args (list[str]): Список аргументов.

	Returns:
		tuple[str | None, int | None]: Возвращает то, что удалось спарсить.
	"""
	host = None
	port = None
	if len(args) >= 2:
		host = args[0]
		port = args[1]
	elif len(args) == 1:
		host = args[0]
		if ":" in host:
			if len(host.split(":")) > 2:
				return None, None
			host, port = host.split(":")

	if port is not None and port.isdigit():
		port = int(port)
	else:
		port = None

	return host, port

async def check_server_info(
	update: Update,
	context: ContextTypes.DEFAULT_TYPE
):
	"""Отправляет пользователю информацию о сервере."""
	message = update.message
	chat_id = update.effective_chat.id

	args = context.args

	logger.info(f"{chat_id}: {message.text}")

	host, port = parse_host_and_port(args)
	is_use_default_host = False
	if host is None:
		is_use_default_host = True
		host = SERVER_HOST
		port = SERVER_PORT

	server = MinecraftServer(host=host, port=port)
	await server.update()
	answ = format_server_info(
			host=host,
			port=port,
			is_online=server.is_online,
			motd=server.motd,
			players=server.players,
			max_online=server.max_online
		)
	if len(args) > 0 and is_use_default_host:
		answ = "Адрес введён неправильно, поэтому используется адрес по умолчанию\n" + answ

	await message.reply_text(answ)


check_server_handler = CommandHandler("status", check_server_info)