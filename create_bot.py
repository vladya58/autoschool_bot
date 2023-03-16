from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database

db = Database('C:\pybot\db.db')
bot = Bot(token='6132924794:AAEGdkuvbN_lOCnlThLVFHCPwvNKafdgmic')
dp = Dispatcher(bot,storage=MemoryStorage())