# aternos_notify

**aternos_notify** - это Telegarm-бот, присылающий оповещения, когда выбранный Aternos-сервер выключился/запустился/собирается запускаться.

---

## Установка

---

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Kirabrin2v/aternos_status_notify.git
cd aternos_status_notify
```

2. **Создайте виртуальное окружение и установите зависимости:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Создайте файл .env в корне проекта и введите Telegram-токен:**
`
TG_TOKEN=ваш_токен_бота
`
4. **Создайте файл config.py в корне проекта.**
   - Пример правильной конфигурации в файле config_example.py.
   - Перед айди группы нужно добавить -100. 
   ```python
   SERVER_HOST: str = "Test.aternos.me"
   SERVER_PORT: int | None = 11765
   TG_CHAT_ID: int = -1009999999999
   ```
---

