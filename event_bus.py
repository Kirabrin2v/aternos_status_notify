from typing import Any, Callable


class EventBus:
    def __init__(self):
        self._subscribers = {}
        self.event_names = set()

    def subscribe(self, event_name: str, callback: Callable[..., Any]):
        """
        Подписывает функцию на событие.

        При публикации указанного события вызовется callback.

        Args:
            event_name (str)
            callback (Callable): Функция, которая обработает событие.
        """
        if event_name in self._subscribers:
            self._subscribers[event_name].append(callback)
        else:
            self._subscribers[event_name] = [callback]

    async def publish(self, event_name: str, *args: Any):
        """
        Публикует событие.

        Вызывает все функции, подписанные на это событие. В каждую функцию
        передаёт все переданные инициатором события аргументы.

        Args:
            event_name (str)
            args (Any): Аргументы, которые будут переданы в вызываемую функцию.
        """
        for callback in self._subscribers.get(event_name, []):
            try:
                await callback(*args)
            except Exception as e:
                print(f"Ошибка в хендлере: {callback}", e)


event_bus = EventBus()
