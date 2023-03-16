from create_bot import dp,bot,db

from aiogram import types, Dispatcher

#@dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
   await message.answer('Извините, я Вас не понял. Вернитесь в главное меню командой /menu')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(echo)