# Cмена клавиатуры 
# @dispatcher.callback_query_handler(lambda call: "<CALLBACK>" in call.data)
# async def next_keyboard(call):

#     await call.message.edit_reply_markup(<YOUR KEYBOARD>)

#6132924794:AAEGdkuvbN_lOCnlThLVFHCPwvNKafdgmic
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import logging
from typing import Union
from db import Database
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import time

class UserState(StatesGroup):
    name = State()
    pasport = State()
    medical = State()
    email = State()
    age = State()


    
class lkState(StatesGroup):
    lk = State()
    reg_data = State()
    edit_data = State()
    view_data = State()
    exam = State()
    history_balance = State()


db = Database('C:\pybot\db.db')

Rules = True
status = 'Авторизован'
first_name = "User"
balance = 0

bot = Bot(token='6132924794:AAEGdkuvbN_lOCnlThLVFHCPwvNKafdgmic')
dp = Dispatcher(bot,storage=MemoryStorage())

 #message.answer(text="Вы уже авторизованы.", show_alert=True) 


            


@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def cmd_start(message: types.Message):
    if (not db.user_exists(message.from_user.id)):
         
        keyboard = types.ReplyKeyboardMarkup()
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        cancel_phone = types.KeyboardButton(text="Отклонить")
        keyboard.add(button_phone,cancel_phone)
        await message.answer("Для авторизации нам нужен Ваш номер телефона.",reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегестрированны в системе. Для перехода в меню воспользуйтесь командой /menu') #message.answer(text="Вы уже авторизованы.", show_alert=True) 
    


@dp.message_handler(content_types=types.ContentType.CONTACT) #Еще нужна обработка отмены отправки контакта.
async def get_auto(message: types.Message, state: FSMContext):
    if db.phone_exists(message.contact.phone_number.replace("+", "")):
        db.set_user_id(message.contact.user_id,message.contact.phone_number.replace("+", ""))

        await message.answer(f"Твой номер успешно авторизован. Для дальнейшей регистрации заполни данные в личном кабинете. Используй команду /menu.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("К сожалению Вас нет в списках студентов. Обратитесь по номер 8 800 555 3535", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(Text(equals="Отклонить"))
@dp.message_handler(commands=['menu']) #Явно указываем в декораторе, на какую команду реагируем. 
async def cmd_menu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    if ( db.user_exists(message.from_user.id)):
        
    
        buttons_menu = types.ReplyKeyboardMarkup()
        button_1 = types.KeyboardButton(text="👤 Личный кабинет")
        button_2 = '🚘 Записаться на вождение'
        button_3 = '📅 Просмотреть график занятий'
        button_4 = '💵 Пополнить баланс'
        button_5 = '✅ Пройти экзамен ПДД'
        button_6 = '✉️ Сообщение для админа.'
        button_7 = '❓ Информация.'
        buttons_menu.add(button_1,button_2,button_3, button_4, button_5, button_6, button_7)
        await message.answer("{0.first_name}, Вы находитесь в главном меню.".format(message.from_user), reply_markup=buttons_menu)
    else:
        await message.answer("Вы не авторизованы. Воспользуйтесь командой /start.", reply_markup=types.ReplyKeyboardRemove())

@dp.callback_query_handler(lambda callback: callback.data in ["back_to_lk"])
async def with_puree(callback: Union[types.CallbackQuery,types.Message],state: FSMContext):
    await callback.message.delete()
    keyboard_lk = types.InlineKeyboardMarkup()
    lk_b1 = types.InlineKeyboardButton(text="Заполнить данные", callback_data="log in")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    lk_b2 = types.InlineKeyboardButton(text="Просмотреть данные", callback_data="view_data")
    lk_b3 = types.InlineKeyboardButton(text="Изменить данные", callback_data="edit_data")
    lk_b4 = types.InlineKeyboardButton(text="Просмотр маршрута", callback_data="ex_mars")
    lk_b5 = types.InlineKeyboardButton(text="История пополнений", callback_data="history_balance")
    lk_b6 = types.InlineKeyboardButton(text="Меню", callback_data="/menu")

    keyboard_lk.add(lk_b1,lk_b2,lk_b3,lk_b4,lk_b5,lk_b6) if db.get_full(callback.from_user.id) == "Регистрация не завершена" else keyboard_lk.add(lk_b2,lk_b3,lk_b4,lk_b5,lk_b6)

    
    await callback.message.answer(f'👤Личный кабинет👤:\nНикнейм {first_name}!\nСтатус: {db.get_full(callback.from_user.id)}\nБаланс: {balance}', reply_markup=keyboard_lk)#reply_markup=types.ReplyKeyboardRemove()

# from aiogram.dispatcher.filters import Text
@dp.message_handler(Text(equals="👤 Личный кабинет"))
async def with_puree(message: Union[types.Message,types.CallbackQuery], state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_lk = types.InlineKeyboardMarkup()
    lk_b1 = types.InlineKeyboardButton(text="Заполнить данные", callback_data="log in")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    lk_b2 = types.InlineKeyboardButton(text="Просмотреть данные", callback_data="view_data")
    lk_b3 = types.InlineKeyboardButton(text="Изменить данные", callback_data="edit_data")
    lk_b4 = types.InlineKeyboardButton(text="Просмотр маршрута", callback_data="ex_mars")
    lk_b5 = types.InlineKeyboardButton(text="История пополнений", callback_data="history_balance")
    lk_b6 = types.InlineKeyboardButton(text="Меню", callback_data="/menu")
    

    keyboard_lk.add(lk_b1,lk_b2,lk_b3,lk_b4,lk_b5,lk_b6) if db.get_full(message.from_user.id) == "Регистрация не завершена" else keyboard_lk.add(lk_b2,lk_b3,lk_b4,lk_b5,lk_b6)


    await message.answer(f'👤Личный кабинет👤:\nНикнейм {first_name}!\nСтатус: {db.get_full(message.from_user.id)}\nБаланс: {balance}', reply_markup=keyboard_lk)#reply_markup=types.ReplyKeyboardRemove()



@dp.callback_query_handler(lambda callback: callback.data in ["log in", "view_data"])
async def auto(callback: types.CallbackQuery):
    if callback.data == "log in":
        await callback.message.delete()
        lst_data = db.get_data(callback.from_user.id)
        keyboard_reg = types.InlineKeyboardMarkup()
        reg_b1 = types.InlineKeyboardButton(text="Указать ФИО", callback_data="set_name")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
        reg_b2 = types.InlineKeyboardButton(text="Указать паспорт", callback_data="set_pasport")
        reg_b3 = types.InlineKeyboardButton(text="Указать медсправку", callback_data="set_medical")
        reg_b4 = types.InlineKeyboardButton(text="Указать эл. почту", callback_data="set_email")
        reg_b5 = types.InlineKeyboardButton(text="Указать дату рождения", callback_data="set_age")
        reg_b6 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_lk")
        lst_key = [reg_b1,reg_b2,reg_b3,reg_b4,reg_b5]
        for i in range(len(lst_data)-1,-1,-1):
            if lst_data[i] == None or lst_data[i] == "":
                pass
            else:
                lst_key.pop(i)
        if len(lst_key) !=0:
            keyboard_reg.add(*lst_key,reg_b6) 
            await callback.message.answer('Какие данные вы хотите заполнить?',reply_markup=keyboard_reg)
        else:
            db.set_full(callback.from_user.id, 'Регистрация завершена')
            await callback.message.answer('Вы заполнили все поля. Для перехода в главное меню воспользуйтесь командой /menu',reply_markup=keyboard_reg)

   
    if callback.data == "view_data":
        await callback.message.delete()
        lst_full_data = db.get_full_data(callback.from_user.id)
        keyboard_reg = types.InlineKeyboardMarkup()
        reg_b1 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_lk")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    
    
        keyboard_reg.add(reg_b1) 
        await callback.message.answer(f'Ваши данные:\nЛогин {lst_full_data[0]}\nТелефон +{lst_full_data[1]}\nИмя {lst_full_data[2]}\nПаспортные данные {lst_full_data[3]}\nМедицинская справка {lst_full_data[4]}\nЭлектронный адрес {lst_full_data[5]}\nДата рождения {lst_full_data[6]}\nГруппа {lst_full_data[7]}\n',reply_markup=keyboard_reg)
        
    # if Rules:
    
    #     await call.answer(text="Вы уже авторизованы.", show_alert=True) #Всплывающее сообщение







@dp.callback_query_handler(text="set_name")
async def get_name(call: types.CallbackQuery, state: FSMContext):
    
    await call.message.delete()
    await call.message.answer('Введите ваше ФИО.')
    await UserState.name.set()

@dp.callback_query_handler(text="set_pasport")
async def get_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Введите ваше серию и номер паспорта в формате: 1234 56789123.')
    await UserState.pasport.set()


@dp.callback_query_handler(text="set_medical")
async def get_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите номер вашей медсправки в формате: 00 1234567.')
    await UserState.medical.set()

@dp.callback_query_handler(text="set_email")
async def get_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите ваше электронный адрес.')
    await UserState.email.set()

@dp.callback_query_handler(text="set_age")
async def get_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите вашу дату рождения в формате: 01.01.1900.')
    await UserState.age.set()

    
@dp.message_handler(state=UserState.name,content_types=types.ContentTypes.TEXT)
async def set_name(message: types.Message, state: FSMContext,call = "set_name"):
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    keyboard_reg = types.InlineKeyboardMarkup()
    reg_b1 = types.InlineKeyboardButton(text="Да", callback_data="log in")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    reg_b2 = types.InlineKeyboardButton(text="Нет", callback_data=call)
    keyboard_reg.add(reg_b1,reg_b2)
    db.set_name(message.from_user.id, message.text)
    await state.finish()
    await message.answer(f'Вы указали {message.text}.Верно?',reply_markup=keyboard_reg) 

@dp.message_handler(state=UserState.pasport,content_types=types.ContentTypes.TEXT)
async def set_pasport(message: types.Message, state: FSMContext,call = "set_pasport"):
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    keyboard_reg = types.InlineKeyboardMarkup()
    reg_b1 = types.InlineKeyboardButton(text="Да", callback_data="log in")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    reg_b2 = types.InlineKeyboardButton(text="Нет", callback_data=call)
    keyboard_reg.add(reg_b1,reg_b2)
    db.set_pasport(message.from_user.id, message.text)
    await state.finish()
    await message.answer(f'Вы указали {message.text}.Верно?',reply_markup=keyboard_reg)
    
          

    


    



    


@dp.message_handler(state=lkState.lk,content_types=types.ContentTypes.TEXT)
async def bot_message(message: types.Message):
    await message.reply("Не понял", reply_markup=types.ReplyKeyboardRemove())

    
# @dp.message_handler() 

    





@dp.message_handler(lambda message: message.text == "🚘 Записаться на вождение")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())








@dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
   await message.answer('Извините, я Вас не понял. Вернитесь в главное меню командой /menu')





if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)






# import telebot
# from telebot import apihelper



# token = '6132924794:AAEGdkuvbN_lOCnlThLVFHCPwvNKafdgmic'

# bot = telebot.TeleBot(token)




# @bot.message_handler(content_types=['text'])
# def send_text(message):
#    


        
#     elif message.text == '🚘 Записаться на вождение':
#         markup2 = telebot.types.InlineKeyboardMarkup()
#         rec = telebot.types.InlineKeyboardButton(text='Запись', callback_data=5)
#         cancel = telebot.types.InlineKeyboardButton(text='Отменить запись', callback_data=6)
        
#         markup2.add(rec, cancel)
#         bot.send_message(message.chat.id, f'{first_name}, здесь Вы можете записаться или отменить запись!',reply_markup=markup2) #.format(message.from_user)





#     elif message.text == '📅 Просмотреть график занятий':
#         markup3 = telebot.types.InlineKeyboardMarkup()
#         teori = telebot.types.InlineKeyboardButton(text='Расписание теории', callback_data=7)
#         practic = telebot.types.InlineKeyboardButton(text='Расписание практики', callback_data=8)      
#         markup3.add(teori, practic)
#         bot.send_message(message.chat.id, f'{first_name}, здесь Вы можете просмотреть расписание ваших записей!',reply_markup=markup3) #.format(message.from_user)




#     elif message.text == '💵 Пополнить баланс':
#         markup4 = telebot.types.InlineKeyboardMarkup()
#         replen = telebot.types.InlineKeyboardButton(text='Пополнить баланс', callback_data=9)
#         retur = telebot.types.InlineKeyboardButton(text='Вывод средств', callback_data=10)
#         markup4.add(replen, retur)
#         bot.send_message(message.chat.id, f'{first_name}, здесь Вы можете управлять вашим балансом!',reply_markup=markup4)




#     elif message.text == '✅ Пройти экзамен ПДД':
#         markup5 = telebot.types.InlineKeyboardMarkup()
#         start_ekz = telebot.types.InlineKeyboardButton(text='Начать', callback_data=11)
#         info_ekz = telebot.types.InlineKeyboardButton(text='Информация', callback_data=12)
#         markup5.add(start_ekz, info_ekz)
#         bot.send_message(message.chat.id, f'{first_name}, попробуйте свои силы в реальном теоретическом экзамене!',reply_markup=markup5)





#     elif message.text == '✉️ Оставить сообщение для админа.':
#         bot.send_message(message.chat.id, 'Пока!')





#     elif message.text == '❓ Информация.':
#         bot.send_message(message.chat.id, 'Пока!')

#     else:
#         bot.send_message(message.chat.id, 'Увы, я Вас не понял. Вернитесь в главное меню командой /start')


# # @bot.message_handler(commands=['start'])
# # def start_message(message):
# #     keyboard = telebot.types.ReplyKeyboardMarkup(True)
# #     keyboard.row('Привет', 'Пока')
# #     bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

# # @bot.message_handler(commands=['test'])
# # def start_message(message):
# #     markup = telebot.types.InlineKeyboardMarkup()
# #     markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
# #     markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
# #     markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
# #     bot.send_message(message.chat.id, text="Какая средняя оценка была у Вас в школе?", reply_markup=markup)
# # @bot.message_handler(content_types=['text'])
# # def send_text(message):
# #     if message.text.lower() == 'привет':
# #         bot.send_message(message.chat.id, 'Ещё раз привет!')
# #     elif message.text.lower() == 'пока':
# #         bot.send_message(message.chat.id, 'Пока!')

# # @bot.callback_query_handler(func=lambda call: True)
# # def query_handler(call):

# #     bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за честный ответ!')
# #     answer = ''
# #     if call.data == '3':
# #         answer = 'Вы троечник!'
# #     elif call.data == '4':
# #         answer = 'Вы хорошист!'
# #     elif call.data == '5':
# #         answer = 'Вы отличник!'

# #     bot.send_message(call.message.chat.id, answer)
# #     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

# bot.polling()

