@echo off

call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=5229907022:AAEdqvhkr5LqyXmQd8eN5LNXMojE52hbHRs

python bot_telegram.py

pause