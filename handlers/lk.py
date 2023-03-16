from db import Database
from aiogram import types, Dispatcher
from aiogram.types import InputFile
from aiogram.dispatcher.filters import Text
from create_bot import db,dp,bot
from typing import Union
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

first_name = "User"
balance = 0

class UserState(StatesGroup):
    name = State()
    passport = State()
    medical = State()
    email = State()
    age = State()
    name_edit = State()
    passport_edit = State()
    medical_edit = State()
    email_edit = State()
    age_edit = State()

#@dp.callback_query_handler(lambda callback: callback.data in ["back_to_lk"])
async def with_puree(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    keyboard_lk = types.InlineKeyboardMarkup()
    lk_b1 = types.InlineKeyboardButton(text="Заполнить данные", callback_data="log in")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    lk_b2 = types.InlineKeyboardButton(text="Просмотреть данные", callback_data="view_data")
    lk_b3 = types.InlineKeyboardButton(text="Изменить данные", callback_data="edit_data")
    lk_b4 = types.InlineKeyboardButton(text="Просмотр маршрута", callback_data="view_marshrut")
    lk_b5 = types.InlineKeyboardButton(text="История пополнений", callback_data="history_balance")
    lk_b6 = types.InlineKeyboardButton(text="Меню", callback_data="menu", switch_inline_query="/menu")

    keyboard_lk.add(lk_b1,lk_b2,lk_b3,lk_b4,lk_b5,lk_b6) if db.get_full(callback.from_user.id) == False else keyboard_lk.add(lk_b2,lk_b3,lk_b4,lk_b5,lk_b6)

    
    await callback.message.answer(f'👤Личный кабинет👤:\nНикнейм {first_name}!\nСтатус: {db.get_full(callback.from_user.id)}\nБаланс: {balance}', reply_markup=keyboard_lk)#reply_markup=types.ReplyKeyboardRemove()

# from aiogram.dispatcher.filters import Text
#@dp.message_handler(Text(equals="👤 Личный кабинет"))
async def lk(message: Union[types.Message,types.CallbackQuery], state: FSMContext, previous_state=None):
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_lk = types.InlineKeyboardMarkup()
    lk_b1 = types.InlineKeyboardButton(text="Заполнить данные", callback_data="log in")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    lk_b2 = types.InlineKeyboardButton(text="Просмотреть данные", callback_data="view_data")
    lk_b3 = types.InlineKeyboardButton(text="Изменить данные", callback_data="edit_data")
    lk_b4 = types.InlineKeyboardButton(text="Просмотр маршрута", callback_data="view_marshrut")
    lk_b5 = types.InlineKeyboardButton(text="История пополнений", callback_data="history_balance")
    lk_b6 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    

    keyboard_lk.add(lk_b1,lk_b2,lk_b3,lk_b4,lk_b5,lk_b6) if db.get_full(message.from_user.id) == False else keyboard_lk.add(lk_b2,lk_b3,lk_b4,lk_b5,lk_b6)


    await message.answer(f'👤Личный кабинет👤:\nНикнейм {first_name}!\nСтатус: {db.get_full(message.from_user.id)}\nБаланс: {balance}', reply_markup=keyboard_lk)#reply_markup=types.ReplyKeyboardRemove()
    
    
#@dp.callback_query_handler(lambda callback: callback.data in ["log in", "view_data"])
async def auto(callback: types.CallbackQuery, state: FSMContext):
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
            db.set_full(callback.from_user.id)
            await callback.message.answer('Вы заполнили все поля. Для перехода в главное меню воспользуйтесь командой /menu',reply_markup=keyboard_reg)

    if callback.data == "edit_data":
        await callback.message.delete()
        lst_data = db.get_data(callback.from_user.id)
        keyboard_reg = types.InlineKeyboardMarkup()
        reg_b1 = types.InlineKeyboardButton(text="Изменить ФИО", callback_data="edit_name")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
        reg_b2 = types.InlineKeyboardButton(text="Изменить паспорт", callback_data="edit_pasport")
        reg_b3 = types.InlineKeyboardButton(text="Изменить медсправку", callback_data="edit_medical") 
        reg_b4 = types.InlineKeyboardButton(text="Изменить эл. почту", callback_data="edit_email")
        reg_b5 = types.InlineKeyboardButton(text="Изменить дату рождения", callback_data="edit_age")
        reg_b6 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_lk")
        lst_key = [reg_b1,reg_b2,reg_b3,reg_b4,reg_b5]
        for i in range(len(lst_data)-1,-1,-1):
            if lst_data[i] != None or lst_data[i] != "":
                pass
            else:
                lst_key.pop(i)
        if len(lst_key) !=0:
            keyboard_reg.add(*lst_key,reg_b6) 
            await callback.message.answer('Какие данные вы хотите изменить?',reply_markup=keyboard_reg)
        else:
            await callback.message.answer('Вы еще не заполнили ни одного поля доступного для изменения',reply_markup=keyboard_reg)
        


    if callback.data == "view_data":
        await callback.message.delete()
        lst_full_data = db.get_full_data(callback.from_user.id)
        keyboard_reg = types.InlineKeyboardMarkup()
        reg_b1 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_lk")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    
    
        keyboard_reg.add(reg_b1) 
        await callback.message.answer(f'Ваши данные:\nЛогин {lst_full_data[0]}\nТелефон +{lst_full_data[1]}\nИмя {lst_full_data[2]}\nПаспортные данные {lst_full_data[3]}\nМедицинская справка {lst_full_data[4]}\nЭлектронный адрес {lst_full_data[5]}\nДата рождения {lst_full_data[6]}\nГруппа {lst_full_data[7]}\n',reply_markup=keyboard_reg)
        
    if callback.data == "view_marshrut":
        await state.update_data(previous_state="lk")
        await callback.message.delete()
        keyboard_reg = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_lk")
        keyboard_reg.add(b1) 

        with open('1.jpg', 'rb') as photo:
            await callback.message.answer_photo(InputFile(photo),reply_markup= keyboard_reg)

    if callback.data == "history_balance":
        await state.update_data(previous_state="lk")
        await callback.message.delete()

        keyboard_reg = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_lk")
        keyboard_reg.add(b1) 
        await callback.message.answer('У Вас не было пополнений баланса',reply_markup=keyboard_reg)

    if callback.data == "menu":
        await bot.send_message(callback.from_user.id, '/menu')
        
    
    elif callback.data == "back_to_lk":
        # получаем предыдущее состояние и вызываем функцию lk с этим состоянием
        data = await state.get_data()
        previous_state = data.get("previous_state")
        await lk(callback.message, state, previous_state)



    







#@dp.callback_query_handler(text="set_name")
async def set_data(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == "set_name":
        question = "Введите ваше ФИО."
        await UserState.name.set()
    elif call.data == "set_pasport":
        question = "Введите ваше серию и номер паспорта в формате: 1234 56789123."
        await UserState.passport.set()
    elif call.data == "set_medical":
        question = "Введите номер вашей медсправки в формате: 00 1234567."
        await UserState.medical.set()
    elif call.data == "set_email":
        question = "Введите ваш электронный адрес."
        await UserState.email.set()
    elif call.data == "set_age":
        question = "Введите вашу дату рождения в формате: 01.01.1900"
        await UserState.age.set()
        
    await call.message.answer(question)




async def set_personal_data(message: types.Message, state: FSMContext):
    # state_key = state.key
    state_key = await state.get_state()
    if  state_key == UserState.name.state:
        db.set_name(message.from_user.id, message.text)
        call_back_data = "set_name"
    elif state_key == UserState.passport.state:
        db.set_pasport(message.from_user.id, message.text)
        call_back_data = "set_pasport"

    elif state_key == UserState.medical.state:
        db.set_medical(message.from_user.id, message.text)
        call_back_data = "set_medical"
    elif state_key == UserState.email.state:
        db.set_email(message.from_user.id, message.text)
        call_back_data = "set_email"
    elif state_key == UserState.age.state:
        db.set_age(message.from_user.id, message.text)
        call_back_data = "set_age"


    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    keyboard_reg = types.InlineKeyboardMarkup()
    reg_b1 = types.InlineKeyboardButton(text="Да", callback_data="log in")
    reg_b2 = types.InlineKeyboardButton(text="Нет", callback_data=call_back_data)
    keyboard_reg.add(reg_b1, reg_b2)
    await state.finish()
    await message.answer(f'Вы указали {message.text}.Верно?', reply_markup=keyboard_reg)








async def edit_data(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == "edit_name":
        question = "Введите ваше ФИО."
        await UserState.name_edit.set()
    elif call.data == "edit_pasport":
        question = "Введите ваше серию и номер паспорта в формате: 1234 56789123."
        await UserState.passport_edit.set()
    elif call.data == "edit_medical":
        question = "Введите номер вашей медсправки в формате: 00 1234567."
        await UserState.medical_edit.set()
    elif call.data == "edit_email":
        question = "Введите ваш электронный адрес."
        await UserState.email_edit.set()
    elif call.data == "edit_age":
        question = "Введите вашу дату рождения в формате: 01.01.1900"
        await UserState.age_edit.set()
        
    await call.message.answer(question)




async def edit_personal_data(message: types.Message, state: FSMContext):
    # state_key = state.key
    state_key = await state.get_state()
    if  state_key == UserState.name_edit.state:
        db.set_name(message.from_user.id, message.text)
        call_back_data = "edit_name"
    elif state_key == UserState.passport_edit.state:
        db.set_pasport(message.from_user.id, message.text)
        call_back_data = "edit_pasport"

    elif state_key == UserState.medical_edit.state:
        db.set_medical(message.from_user.id, message.text)
        call_back_data = "edit_medical"
    elif state_key == UserState.email_edit.state:
        db.set_email(message.from_user.id, message.text)
        call_back_data = "edit_email"
    elif state_key == UserState.age_edit.state:
        db.set_age(message.from_user.id, message.text)
        call_back_data = "edit_age"


    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    keyboard_reg = types.InlineKeyboardMarkup()
    reg_b1 = types.InlineKeyboardButton(text="Да", callback_data="edit_data")
    reg_b2 = types.InlineKeyboardButton(text="Нет", callback_data=call_back_data)
    keyboard_reg.add(reg_b1, reg_b2)
    await state.finish()
    await message.answer(f'Вы указали {message.text}.Верно?', reply_markup=keyboard_reg)







def register_handlers(dp: Dispatcher):
    
    dp.register_message_handler(lk, lambda message:"👤 Личный кабинет" in message.text  )
    dp.register_callback_query_handler(with_puree, lambda callback: callback.data in ["back_to_lk"]  )
    dp.register_callback_query_handler(auto, lambda callback: callback.data in ["log in","view_data","edit_data","view_marshrut","history_balance"] )
    dp.register_callback_query_handler(edit_data, lambda callback: callback.data in ["edit_name","edit_pasport","edit_medical","edit_email","edit_age"] )
    dp.register_callback_query_handler(set_data, lambda callback: callback.data in ["set_name","set_pasport","set_medical","set_email","set_age"] )
    

    dp.register_message_handler(set_personal_data, state=[UserState.name, UserState.passport, UserState.medical,UserState.email,UserState.age], content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(edit_personal_data, state=[UserState.name_edit, UserState.passport_edit, UserState.medical_edit,UserState.email_edit,UserState.age_edit], content_types=types.ContentTypes.TEXT)
    # dp.register_message_handler(set_pasport_prov, state=UserState.pasport,content_types=types.ContentTypes.TEXT )



    #dp.register_message_handler(get_auto, content_types=types.ContentType.CONTACT )