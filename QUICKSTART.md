# 🚀 Быстрый старт

## За 5 минут к рабочему боту!

### 1️⃣ Установите зависимости
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2️⃣ Создайте Telegram бота
1. Напишите [@BotFather](https://t.me/BotFather)
2. `/newbot` → следуйте инструкциям
3. Скопируйте токен

### 3️⃣ Настройте Google Sheets API
1. [Google Cloud Console](https://console.cloud.google.com/) → Create Project
2. Enable **Google Sheets API**
3. Create **Service Account** → Download JSON key
4. Сохраните как `config/google_credentials.json`
5. Откройте JSON, скопируйте `client_email`
6. Откройте [таблицу](https://docs.google.com/spreadsheets/d/1YYvqtrrEG2ssNLbKnsIX3goVQfpeJ-E8wcM06P2ts7Q/edit) → Share → вставьте email → Viewer

### 4️⃣ Создайте .env файл
```bash
copy .env.example .env  # Windows
```

Откройте `.env` и вставьте ваш токен:
```
BOT_TOKEN=ваш_токен_от_BotFather
```

### 5️⃣ Запустите бота
```bash
python main.py
```

### 6️⃣ Готово! 🎉
Найдите бота в Telegram и отправьте `/start`

## 🔍 Как искать:
Нажмите "Начать поиск" → введите данные в формате:
```
Фамилия Имя Отчество Класс
```
Например: `Иванов Иван Иванович 10А`

---

## 📖 Подробные инструкции
- **Полное руководство:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Формат таблицы:** [SPREADSHEET_FORMAT.md](SPREADSHEET_FORMAT.md)
- **Документация:** [README.md](README.md)

## ⚠️ Частые проблемы
- **"BOT_TOKEN is not set"** → Проверьте файл `.env`
- **"Credentials file not found"** → Проверьте `config/google_credentials.json`
- **"Failed to connect"** → Дайте доступ Service Account к таблице

## 🆘 Нужна помощь?
Читайте логи: `logs/bot.log`
