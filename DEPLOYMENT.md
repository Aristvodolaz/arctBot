# 🚀 Руководство по деплою бота на сервер

## Содержание
- [Метод 1: Docker Compose (Рекомендуется)](#метод-1-docker-compose)
- [Метод 2: Systemd Service (Linux)](#метод-2-systemd-service)
- [Метод 3: Screen/Tmux](#метод-3-screentmux)
- [Мониторинг и управление](#мониторинг-и-управление)

---

## Подготовка

### 1. Загрузите проект на сервер

```bash
# Через Git
git clone <repository-url>
cd arctBot

# Или через SCP/SFTP
scp -r /path/to/arctBot user@server:/path/to/destination
```

### 2. Убедитесь, что файлы на месте

```bash
ls -la
```

Должны быть:
- ✅ `.env` файл с BOT_TOKEN
- ✅ `config/google_credentials.json`
- ✅ `requirements.txt`
- ✅ Все исходные файлы

---

## Метод 1: Docker Compose (Рекомендуется) 🐳

### Преимущества:
- ✅ Изолированная среда
- ✅ Легкое обновление
- ✅ Автоматический перезапуск
- ✅ Не зависит от системных библиотек

### Установка Docker

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**CentOS/RHEL:**
```bash
sudo yum install docker docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

После установки перелогиньтесь или выполните:
```bash
newgrp docker
```

### Деплой

```bash
# Автоматический деплой
chmod +x deploy.sh
./deploy.sh
# Выберите опцию 1 (Docker Compose)

# Или вручную
docker-compose up -d --build
```

### Управление

```bash
# Просмотр логов
docker-compose logs -f

# Остановить бота
docker-compose down

# Перезапустить
docker-compose restart

# Проверить статус
docker-compose ps

# Обновить код и перезапустить
git pull  # если используете Git
docker-compose up -d --build
```

---

## Метод 2: Systemd Service (Linux) 🐧

### Преимущества:
- ✅ Нативная интеграция с Linux
- ✅ Автозапуск при перезагрузке
- ✅ Управление через systemctl

### Установка

**1. Установите Python и зависимости:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# CentOS/RHEL
sudo yum install python3 python3-pip -y
```

**2. Создайте виртуальное окружение:**

```bash
cd /path/to/arctBot
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**3. Настройте systemd service:**

Отредактируйте `systemd.service`:
```bash
nano systemd.service
```

Замените:
- `YOUR_USER` → ваш пользователь (например: `ubuntu`)
- `/path/to/arctBot` → полный путь к проекту (например: `/home/ubuntu/arctBot`)

**4. Установите и запустите service:**

```bash
# Скопируйте файл в systemd
sudo cp systemd.service /etc/systemd/system/arctbot.service

# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable arctbot

# Запустите бота
sudo systemctl start arctbot

# Проверьте статус
sudo systemctl status arctbot
```

### Управление

```bash
# Запустить
sudo systemctl start arctbot

# Остановить
sudo systemctl stop arctbot

# Перезапустить
sudo systemctl restart arctbot

# Проверить статус
sudo systemctl status arctbot

# Просмотр логов
sudo journalctl -u arctbot -f

# Или из файла
tail -f logs/bot.log
```

---

## Метод 3: Screen/Tmux 📺

### Для быстрого тестирования

**С Screen:**

```bash
# Установка
sudo apt install screen -y  # Ubuntu/Debian
sudo yum install screen -y   # CentOS/RHEL

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Запуск в screen
screen -S arctbot
python main.py

# Выход из screen: Ctrl+A затем D

# Вернуться к screen
screen -r arctbot

# Завершить screen
screen -X -S arctbot quit
```

**С Tmux:**

```bash
# Установка
sudo apt install tmux -y

# Запуск
tmux new -s arctbot
source venv/bin/activate
python main.py

# Выход: Ctrl+B затем D

# Вернуться
tmux attach -t arctbot
```

---

## Мониторинг и управление

### Просмотр логов

**Docker:**
```bash
docker-compose logs -f
docker logs arctbot -f --tail 100
```

**Systemd:**
```bash
sudo journalctl -u arctbot -f
tail -f logs/bot.log
```

**Direct:**
```bash
tail -f logs/bot.log
```

### Проверка работы бота

1. Отправьте `/start` боту в Telegram
2. Проверьте логи на наличие ошибок
3. Попробуйте выполнить поиск

### Обновление бота

**Docker:**
```bash
# Остановить
docker-compose down

# Обновить код (если Git)
git pull

# Пересобрать и запустить
docker-compose up -d --build
```

**Systemd:**
```bash
# Остановить
sudo systemctl stop arctbot

# Обновить код
git pull

# Обновить зависимости (если изменились)
source venv/bin/activate
pip install -r requirements.txt

# Запустить
sudo systemctl start arctbot
```

---

## Безопасность

### Защита credentials

```bash
# Права доступа к файлам
chmod 600 .env
chmod 600 config/google_credentials.json
chmod 700 config/

# Владелец файлов
chown -R your_user:your_user .
```

### Firewall (если нужен)

Бот использует только исходящие соединения, входящие порты не нужны.

---

## Проблемы и решения

### Бот не запускается

1. **Проверьте .env файл:**
```bash
cat .env | grep BOT_TOKEN
```

2. **Проверьте credentials:**
```bash
ls -la config/google_credentials.json
```

3. **Проверьте логи:**
```bash
tail -f logs/bot.log
```

### Бот перезапускается постоянно

```bash
# Docker
docker-compose logs --tail 50

# Systemd
sudo journalctl -u arctbot -n 50
```

Обычно причина в:
- Неверный BOT_TOKEN
- Отсутствует google_credentials.json
- Нет доступа к Google Sheets

### Обновление не применяется

```bash
# Docker - обязательно пересоберите образ
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Systemd - перезапустите службу
sudo systemctl restart arctbot
```

---

## Рекомендации по продакшену

1. ✅ **Используйте Docker Compose** - самый надёжный способ
2. ✅ **Настройте автоматический перезапуск** (уже включен в docker-compose.yml)
3. ✅ **Мониторьте логи** регулярно
4. ✅ **Делайте бэкапы** .env и google_credentials.json
5. ✅ **Обновляйте зависимости** периодически:
   ```bash
   pip list --outdated
   ```

---

## Автоматическое обновление (опционально)

Создайте cron job для автоматического обновления:

```bash
crontab -e
```

Добавьте:
```cron
# Обновление каждый день в 3:00 AM
0 3 * * * cd /path/to/arctBot && git pull && docker-compose up -d --build
```

---

## Полезные команды

```bash
# Проверить использование ресурсов (Docker)
docker stats arctbot

# Проверить использование диска
du -sh logs/

# Очистить старые логи
find logs/ -name "*.log" -mtime +30 -delete

# Экспорт логов
docker logs arctbot > bot_logs_$(date +%Y%m%d).txt
```

---

## 🆘 Поддержка

Если возникли проблемы:
1. Проверьте логи: `logs/bot.log`
2. Проверьте статус: `docker-compose ps` или `systemctl status arctbot`
3. Убедитесь, что все переменные окружения заданы правильно

Удачи с деплоем! 🚀
