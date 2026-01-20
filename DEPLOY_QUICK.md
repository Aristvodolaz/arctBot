# ⚡ Быстрый деплой - Шпаргалка

## 🐳 Docker Compose (Рекомендуется)

```bash
# 1. Установите Docker (один раз)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Или для Ubuntu/Debian
sudo apt update && sudo apt install docker.io docker-compose -y

# 2. Загрузите проект
git clone <repo-url> && cd arctBot
# ИЛИ скопируйте файлы на сервер

# 3. Убедитесь что есть .env и credentials
ls .env config/google_credentials.json

# 4. Запустите!
docker-compose up -d --build

# 5. Проверьте логи
docker-compose logs -f
```

---

## 🐧 Linux Systemd

```bash
# 1. Установите Python
sudo apt update && sudo apt install python3 python3-venv -y

# 2. Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Настройте systemd.service (замените пути)
nano systemd.service

# 4. Установите service
sudo cp systemd.service /etc/systemd/system/arctbot.service
sudo systemctl daemon-reload
sudo systemctl enable arctbot
sudo systemctl start arctbot

# 5. Проверьте статус
sudo systemctl status arctbot
tail -f logs/bot.log
```

---

## 📺 Screen (быстрое тестирование)

```bash
# 1. Установите screen
sudo apt install screen -y

# 2. Установите зависимости
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Запустите в screen
screen -S arctbot
python main.py

# Выход: Ctrl+A затем D
# Вернуться: screen -r arctbot
```

---

## 🔧 Управление

### Docker
```bash
docker-compose logs -f      # Логи
docker-compose restart      # Перезапуск
docker-compose down         # Остановка
docker-compose ps           # Статус
```

### Systemd
```bash
sudo systemctl status arctbot    # Статус
sudo systemctl restart arctbot   # Перезапуск
sudo systemctl stop arctbot      # Остановка
sudo journalctl -u arctbot -f   # Логи
```

### Screen
```bash
screen -r arctbot         # Подключиться
screen -ls                # Список сессий
screen -X -S arctbot quit # Закрыть
```

---

## 🚨 Проблемы?

```bash
# Проверьте логи
tail -f logs/bot.log

# Проверьте .env
cat .env

# Проверьте credentials
ls -la config/google_credentials.json

# Пересоберите (Docker)
docker-compose down
docker-compose up -d --build
```

---

## ⚙️ Перед деплоем убедитесь:

- [ ] Файл `.env` создан с правильным BOT_TOKEN
- [ ] Файл `config/google_credentials.json` на месте
- [ ] Service Account имеет доступ к таблице
- [ ] Google Sheets API включен

---

**Готово! Бот должен работать** ✨

Проверьте: отправьте `/start` в Telegram
