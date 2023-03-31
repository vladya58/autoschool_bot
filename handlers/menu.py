
from db import Database
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp,bot,db


# @dp.message_handler(Text(equals="Отклонить"))
# @dp.message_handler(commands=['menu']) #Явно указываем в декораторе, на какую команду реагируем. 
async def cmd_menu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    if ( db.user_exists(message.from_user.id)):
        
    
        buttons_menu = types.ReplyKeyboardMarkup()
        button_1 = types.KeyboardButton(text="👤 Личный кабинет")
        button_2 = '🚘 Записаться на вождение'
        button_3 = '📅 Просмотреть график занятий'
        button_4 = '💵 Управление балансом'
        button_5 = '✅ Пройти экзамен ПДД'
        button_6 = '✉️ Сообщение для админа.'
        button_7 = '❓ Информация.'
        buttons_menu.add(button_1,button_2,button_3, button_4, button_5, button_6, button_7)
        await message.answer("{0.first_name}, Вы находитесь в главном меню.".format(message.from_user), reply_markup=buttons_menu)
    else:
        await message.answer("Вы не авторизованы. Воспользуйтесь командой /start.", reply_markup=types.ReplyKeyboardRemove())

#@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def cmd_start(message: types.Message):
    if (not db.user_exists(message.from_user.id)):
         
        keyboard = types.ReplyKeyboardMarkup()
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        cancel_phone = types.KeyboardButton(text="Отклонить")
        keyboard.add(button_phone,cancel_phone)
        await message.answer("Для авторизации нам нужен Ваш номер телефона.",reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегестрированны в системе. Для перехода в меню воспользуйтесь командой /menu') #message.answer(text="Вы уже авторизованы.", show_alert=True) 

#@dp.message_handler(content_types=types.ContentType.CONTACT) #Еще нужна обработка отмены отправки контакта.
async def get_auto(message: types.Message):
    if db.phone_exists(message.contact.phone_number.replace("+", "")):
        db.set_user_id(message.contact.user_id,message.contact.phone_number.replace("+", ""))

        await message.answer(f"Твой номер успешно авторизован. Для дальнейшей регистрации заполни данные в личном кабинете. Используй команду /menu.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("К сожалению Вас нет в списках студентов. Обратитесь по номер 8 800 555 3535", reply_markup=types.ReplyKeyboardRemove())

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_menu, commands=['menu'] )
    dp.register_message_handler(cmd_menu, lambda msg: msg.text == "Отклонить" )
    dp.register_message_handler(cmd_start, commands=['start'] )
    dp.register_message_handler(get_auto, content_types=types.ContentType.CONTACT )
    