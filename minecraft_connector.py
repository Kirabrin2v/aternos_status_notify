import asyncio
import re
from mcstatus import JavaServer

from event_bus import event_bus


QUEUE_WAIT_PATTERN = re.compile(
    r"This server is currently waiting in queue\.\n"
    r"Estimated waiting time is ca\. (\d+) minutes\.\n"
    r"Please try again in a few seconds\."
)
SERVER_STARTING_PATTERN = re.compile(
	r"This server is currently starting\.\n"
	r"Get this server more RAM for free! > craft\.link/ram"
)
print(type(event_bus))
class MinecraftServer:
	"""Объект сервера."""

	def __init__(self, host: str, port: int | None = None):
		"""Инициализирует класс."""
		self.host = host
		self.port = port
		self.client = JavaServer(host=host, port=port)
		self.max_online = 20
		self.is_online = None

		self.reset()
		self._task: asyncio.Task | None = None

	async def start_monitor(self):
		"""Запускает бесконечный цикл актуализации полей."""
		if self._task is None:
			self._task = asyncio.create_task(self._loop())

	async def stop_monitor(self):
		"""Останавливает бесконечный цикл актуализации полей."""
		if self._task:
			self._task.cancel()
			self._task = None

	async def _loop(self):
		"""Актуализирует значения полей с определённым периодом."""
		while True:
			await self.update()
			await asyncio.sleep(30)

	async def update(self):
		"""
		Актуализирует значения полей.

		Записывает актуальные значения  и отправляет
		"""
		try:
			server_info = await self.get_info()
			if server_info != {}:
				# print("\n\n_________________________________________")
				# print([server_info.motd.to_plain()])
				# print([server_info.version.name])
				# print(server_info.players)
				# print("-----------------------------------------\n\n")

				queue_wait_match = QUEUE_WAIT_PATTERN.fullmatch(server_info.motd.to_plain())
				server_starting_match = SERVER_STARTING_PATTERN.fullmatch(server_info.motd.to_plain())
				if queue_wait_match or server_starting_match:
					print("Событие ожидания опубликовано")
					if queue_wait_match:
						left_minutes = int(queue_wait_match[1])
					else:
						left_minutes = 1 # Сервер уже запускается
					await event_bus.publish("server_starting", self.address, left_minutes)

				elif server_info.version.protocol != -1:
					await self.set_server_on()

					self.motd = server_info.motd.to_plain()
					self.max_online = server_info.players.max
					if server_info.players.sample is not None:
						self.players = list(map(
							lambda player_object: player_object.name,
							server_info.players.sample
						))
					else:
						self.players = []
				else:
					await self.set_server_off()
			else:
				await self.set_server_off()

		except Exception as e:
			print(e)

	async def set_server_off(self):
		"""Обновляет статус на выключенный"""
		print(f"Сервер {self.address} выключен")
		if self.is_online == True:
			await event_bus.publish("server_off", self.address)
		self.is_online = False
		self.reset()

	async def set_server_on(self):
		"""Обновляет статус на включённый"""
		print("Сервер включён")
		if self.is_online == False:
			await event_bus.publish("server_on", self.address)
		self.is_online = True

	@property
	def address(self) -> str:
		"""
		Совмещает хост и порт.

		Returns:
			str: Строка вида host:port или host.
		"""
		return f"{self.host}:{self.port}" if self.port is not None else self.host

	def reset(self):
		"""Обнуляет все не константные параметры"""
		self.players = []
		self.motd = None

	async def get_info(self) -> dict:
		"""
		Возвращает краткую информацию о сервере.

		Returns:
			dict: Информация из модуля mcstatus
		"""
		try:
			return self.client.status()
		except Exception:
			return {}

	@property
	async def check_online(self) -> bool:
		"""
		Проверяет, включён ли сервер.
		
		Returns:
			bool
		"""
		server_info = await get_info()
		return server_info != {}
