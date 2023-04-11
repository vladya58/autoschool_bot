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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE
import os
import smtplib

from invoice.generate_send import Generate_invoice, Convert_and_send

async def payment_menu(message: types.Message):
    
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_balance = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Пополнить баланс", callback_data="operation_add_money")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    b2 = types.InlineKeyboardButton(text="Вывести средства", callback_data="operation_return_money")
    b3 = types.InlineKeyboardButton(text="История пополнений", callback_data="operation_history_balance")
    b4 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    keyboard_balance.add(b1,b2,b3,b4) 


    await message.answer('Вы перешли в меню управления балансом! \n\nБла... бла... бла...', reply_markup=keyboard_balance)#reply_markup=types.ReplyKeyboardRemove()




   
    
async def confirm_return_money(query: types.CallbackQuery):
    balance = db.get_balance(query.from_user.id)
    db.set_payment(query.from_user.id,datetime.datetime.now().date(), datetime.datetime.now().time(),balance,"RUB", "return_id","return_tg_bot" )
    db.update_balance(query.from_user.id,-balance )
    await query.answer(text="Возврат оформлен. Деньги поступят в течении 14 рабочих дней. Чтобы отменить возврат обратитесь в поддержку.",show_alert=True)
    
    await payment_menu(query.message)
    
    








async def operation_money_callback(query: types.CallbackQuery):
    await query.message.delete()
    if "add_money" in query.data:
        if "@" in db.get_email(query.from_user.id):

            keyboard_add = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text="500 рублей (1 занятие)", callback_data="add_money_500")
            b2 = types.InlineKeyboardButton(text="1000 рублей (2 занятия)", callback_data="add_money_1000")
            b3 = types.InlineKeyboardButton(text="2500 рублей (5 занятий)", callback_data="add_money_2500")
            b4 = types.InlineKeyboardButton(text="5000 рублей (10 занятий)", callback_data="add_money_5000")
            b5 = types.InlineKeyboardButton(text="Назад", callback_data="add_money_back") 
            keyboard_add.add(b1, b2,b3,b4,b5)

            await query.message.answer('Выберите сумму для пополнения баланса:', reply_markup=keyboard_add)
        else: 
            keyboard_add = types.InlineKeyboardMarkup()
            b5 = types.InlineKeyboardButton(text="Назад", callback_data="add_money_back") 
            keyboard_add.add(b5)
            await query.message.answer('Ваш email указан некорректно, либо не указан. Проверьте правильность в личном кабинете', reply_markup=keyboard_add)


    elif "return_money" in query.data:
        
        balance = db.get_balance(query.from_user.id)
        keyboard_add = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Запросить средства", callback_data="confirm_return")
        b5 = types.InlineKeyboardButton(text="Назад", callback_data="add_money_back") 
        if balance == 0:
            keyboard_add.add(b5)
            await query.message.answer(f'Ваш баланс 0 рублей. Возврат недоступен. Если произошла оишбка свяжитесь с поддержкой.', reply_markup=keyboard_add)
        else:
            keyboard_add.add(b1,b5)
            await query.message.answer(f'Вы можете сделать запрос на возврат средств. Возврат средств осущетсвляется до 14 рабочих дней. Возврат средств возможен только в полном объеме. \n\nК возврату доступно {balance} рублей', reply_markup=keyboard_add)
    
    
    elif "history_balance" in query.data:
        history_array = db.get_payment(query.from_user.id)
        message_text = 'Ваши транзакции:\n\n'
        keyboard_add = types.InlineKeyboardMarkup()
        b5 = types.InlineKeyboardButton(text="Назад", callback_data="add_money_back") 
        keyboard_add.add(b5)
        if len(history_array) !=0:

            for transaction in history_array: #PR сюда добавить "-" если было списание и + если было пополнение
                date = transaction[0].strftime('%d.%m.%Y')
                time = transaction[1].strftime('%H:%M:%S')
                amount = transaction[2]
                operation = "Пополнение"
                operation = "Оплата занятия" if "pay_lesson" in transaction[3] else operation
                operation = "Вывод средств" if "return" in transaction[3] else operation
                operation = "Отмена занятия" if "cancel_lesson" in transaction[3] else operation
                sign = "+" if operation in ["Пополнение","Отмена занятия"] else "-"
                message_text += f'{date} {time}: {sign}{amount} руб. - {operation}\n'
            await query.message.answer(message_text,reply_markup=keyboard_add)
        else:
            await query.message.answer("У вас еще не было транзакций.",reply_markup=keyboard_add)




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
        payload='Пополнение через telegram',
        provider_token=payment_token,
        currency='RUB',
        prices=[types.LabeledPrice('Пополнение баланса', int(value)*100)]
    )
    invoice_dict = invoice.to_python()
    return chat_id, invoice_dict
    






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
    successful_payment = message.successful_payment
    id_payment = db.set_payment(message.from_user.id, datetime.datetime.now().date(), datetime.datetime.now().time(),successful_payment.total_amount / 100,successful_payment.currency, successful_payment.provider_payment_charge_id, successful_payment.invoice_payload )
    db.update_balance(message.from_user.id,successful_payment.total_amount / 100 )
    # send_email_payment(message.from_user.id)
    data = db.get_full_data(message.from_user.id)
    now = datetime.datetime.now()
    try:

        Generate_invoice("test.html",f'invoice{id_payment}{message.from_user.id}.html',id_payment, data[2], message.from_user.id,
                      data[5], "000012345",data[1],'4 цифры карты', f'{now.date()} {now.time()}', successful_payment.invoice_payload, 
                      f'Пополнение баланса. Кол-во занятий: {math.floor(int(successful_payment.total_amount / 100) / 500)} ',
                      successful_payment.total_amount / 100, "Пополнение", data[8] )
    except:
        print(f"Чек номер {id_payment} не создан. Ошибка!")


    
    try:
        Convert_and_send(f'invoice{id_payment}{message.from_user.id}.html', f'invoice{id_payment}{message.from_user.id}.pdf',data[5] )

        
    except:
        print(f"Чек номер {id_payment} не отправлен. Ошибка!")

    
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)

    keyboard_add = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Вернуться", callback_data="add_money_back") 
    keyboard_add.add(b1)
    await bot.send_message(message.chat.id, f"Ваша оплата на сумму {int(successful_payment.total_amount / 100 )} рублей прошла успешно. Чек будет выслан на email",reply_markup=keyboard_add)






    
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(payment_menu, lambda message: message.text == "💵 Управление балансом" )
    dp.register_callback_query_handler(operation_money_callback, lambda query: query.data.startswith('operation_'))
    dp.register_callback_query_handler(confirm_return_money, lambda query: query.data == 'confirm_return')
    dp.register_callback_query_handler(add_balance, lambda query: query.data.startswith('add_money_'))
    dp.register_pre_checkout_query_handler(checkout_process,lambda q: True)
    # dp.register_callback_query_handler(process_successful_payment, lambda c: c.data and types.CallbackQuery.from_awaitable(c).is_successful_payment())
    # dp.register_callback_query_handler(process_failed_payment, content_types=ContentType.)

