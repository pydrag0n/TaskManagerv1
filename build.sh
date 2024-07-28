#!/bin/bash
echo "Установка виртуального окружения..."
python3 -m venv .venv
echo "Активация виртуального окружения..."
source .venv/bin/activate
echo "Установка зависимостей..."
pip install -r requirements.txt
echo "Запуск бота..."
python bot/start.py
