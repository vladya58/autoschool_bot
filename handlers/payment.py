from create_bot import dp,bot,db
from db import Database
from aiogram import types, Dispatcher
from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from aiogram.types.message import ContentType
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import ContentTypeFilter
import datetime
from create_bot import dp,bot,db, payment_token
import math

async def payment_menu(message: types.Message):
    
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_balance = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Пополнить баланс", callback_data="add_money")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    b2 = types.InlineKeyboardButton(text="Вывести средства", callback_data="return_money")
    b3 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    keyboard_balance.add(b1,b2,b3) 


    await message.answer('Вы перешли в меню управления балансом! \n\nБла... бла... бла...', reply_markup=keyboard_balance)#reply_markup=types.ReplyKeyboardRemove()

async def add_money_callback(query: types.CallbackQuery):
    await query.message.delete()

    
    keyboard_add = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="500 рублей (1 занятие)", callback_data="add_money_500")
    b2 = types.InlineKeyboardButton(text="1000 рублей (2 занятия)", callback_data="add_money_1000")
    b3 = types.InlineKeyboardButton(text="2500 рублей (5 занятий)", callback_data="add_money_2500")
    b4 = types.InlineKeyboardButton(text="5000 рублей (10 занятий)", callback_data="add_money_5000")
    b5 = types.InlineKeyboardButton(text="Назад", callback_data="add_money_back") 
    keyboard_add.add(b1, b2,b3,b4,b5)

    await query.message.answer('Выберите сумму для пополнения баланса:', reply_markup=keyboard_add)
    



async def add_balance(query: types.CallbackQuery):
    
    if "back" in query.data:
        await payment_menu(query.message)
    else:
        await query.message.delete()
        chat_id, invoice = payment(query)
        keyboard = types.InlineKeyboardMarkup()
        pay_button = types.InlineKeyboardButton(text="Оплатить", pay=True)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="add_money_back")
        keyboard.row(pay_button, back_button)
        await bot.send_invoice(chat_id, **invoice,reply_markup=keyboard)

        
    









def payment(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    value = query.data.split("_")[-1]
    invoice = types.Invoice(
        title='Пополнение баланса',
        description=f'Пополнение баланса. Кол-во занятий: {math.floor(int(value) / 500)} ',
        payload='tg_bot',
        provider_token=payment_token,
        currency='RUB',
        prices=[types.LabeledPrice('Пополнение баланса', int(value)*100)]
    )
    invoice_dict = invoice.to_python()
    return chat_id, invoice_dict
    




    # # Получаем информацию о платеже
    # amount = payment.total_amount
    # currency = payment.currency
    # invoice_payload = payment.invoice_payload
    # telegram_payment_charge_id = payment.telegram_payment_charge_id
    # provider_payment_charge_id = payment.provider_payment_charge_id
    # successful_payment_data = payment.successful_payment_data

    # # Записываем информацию о платеже в базу данных
    # # Реализация этой функции зависит от используемой СУБД
    # write_payment_to_database(amount, currency, invoice_payload, telegram_payment_charge_id,
    #                           provider_payment_charge_id, successful_payment_data)

async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    if pre_checkout_query.invoice_payload == "FAILURE_PAYMENT":
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="Ошибка при проведении платежа."
        )
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    successful_payment = message.successful_payment #Для чека нужно получить отсюда 1. id_student 2. date 3. currency - валюта 
                                                    # 4. Сумма 5.provider_payment_charge_id - номер транзакции
    keyboard_add = types.InlineKeyboardMarkup()
    db.set_payment(message.from_user.id, datetime.datetime.now(),successful_payment.total_amount / 100, successful_payment.provider_payment_charge_id,successful_payment.currency, successful_payment.invoice_payload )
    

    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)

    
    b1 = types.InlineKeyboardButton(text="Вернуться", callback_data="add_money_back") 
    keyboard_add.add(b1)
    await bot.send_message(message.chat.id, "Ваша оплата на сумму ... прошла успешно. Транзакцию можете увидеть в истории операций.",reply_markup=keyboard_add)




    
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(payment_menu, lambda message: message.text == "💵 Пополнить баланс" )
    dp.register_callback_query_handler(add_money_callback, lambda query: query.data == 'add_money')
    dp.register_callback_query_handler(add_balance, lambda query: query.data.startswith('add_money_'))
    dp.register_pre_checkout_query_handler(checkout_process,lambda q: True)
    # dp.register_callback_query_handler(process_successful_payment, lambda c: c.data and types.CallbackQuery.from_awaitable(c).is_successful_payment())
    # dp.register_callback_query_handler(process_failed_payment, content_types=ContentType.)

