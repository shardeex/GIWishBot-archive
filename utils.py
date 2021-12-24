import json
import os
from types import SimpleNamespace

DATABASE_URL = os.getenv('DATABASE_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

REPOSITORY_NAME = 'GIWishBot'
LANGUAGE_CODES = ('en', 'ru')
LANGUAGE_STRINGS = json.load(open('lang.json', mode='r', encoding='utf-8'), object_hook=lambda x: SimpleNamespace(**x))
