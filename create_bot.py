from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database




db = Database('C:\pybot\db.db')
payment_token = '401643678:TEST:c7d71cee-0944-40ea-9955-3a04a75bc28a'
bot = Bot(token='6132924794:AAEGdkuvbN_lOCnlThLVFHCPwvNKafdgmic')
dp = Dispatcher(bot,storage=MemoryStorage())
