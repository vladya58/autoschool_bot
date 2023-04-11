from create_bot import dp,bot,db
from db import Database
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
import calendar
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from invoice.generate_send import Generate_invoice, Convert_and_send
import random
import math
from html import escape



async def les_menu(message: types.Message):
    
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_rec = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Занятия", callback_data="view_lessons")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    b2 = types.InlineKeyboardButton(text="Экзамены", callback_data="view_exams")
    b4 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    keyboard_rec.add(b1,b2,b4) 

    #PR сюда нужно ценую занятия.
    await message.answer('Вы перешли в меню управления расписанием! Для продолжения выберите нужный пункт.', reply_markup=keyboard_rec)#reply_markup=types.ReplyKeyboardRemove()


async def view_works(query: types.CallbackQuery):
    
    if "lessons" in query.data:   
        await query.message.delete()

        lessons_tr = db.get_lessons_tr(query.from_user.id)

        today = datetime.date.today()
        weekday_num = lessons_tr[0] 
        days_ahead = weekday_num - today.weekday() + (7 if weekday_num <= today.weekday() else 0)
        lessons_tr = ((today + datetime.timedelta(days_ahead),) + lessons_tr[1:],) if lessons_tr else ()

        
        lessons_pr = db.get_lessons_pr(query.from_user.id,datetime.datetime.now().date().strftime('%Y-%m-%d'))
        lessons = lessons_tr + tuple(lessons_pr)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if len(lessons) !=0:
            lessons = sorted(lessons, key=lambda x: (x[0], x[1]))
            for i in range(len(lessons)):
                callback = f"work_{lessons[i][0]}_{lessons[i][1]}_{lessons[i][2]}_{lessons[i][3]}_{lessons[i][4]}_{lessons[i][5]}" 
                
                text = f"Практическое занятие {lessons[i][0]}  {lessons[i][1]}" if lessons[i][4] == 1 else f"Теоретическое занятие {lessons[i][0]}  {lessons[i][1]}" 
                markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
            markup.insert(types.InlineKeyboardButton("Назад", callback_data='view_back'))
            await query.message.answer('Выберите занятие для дальнейших действий. Или вернитесь назад.', reply_markup=markup)
        else:
            markup.insert(types.InlineKeyboardButton("Назад", callback_data='view_back'))
            await query.message.answer('Занятий не обнаружено. Вернитесь назад.', reply_markup=markup)

    if "exams" in query.data:
        await query.message.delete()
        exams = db.get_exams_student(query.from_user.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if len(exams) !=0:

            
            for i in range(len(exams)):
                callback = f"work_ex_{exams[i][0]}_{exams[i][1]}_{exams[i][2]}_{exams[i][3]}" 
                
                text = f"Теоретический экзамен {exams[i][1]}" if exams[i][0] == 3 else f"Практический экзамен {exams[i][1]}" 
                markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
            markup.insert(types.InlineKeyboardButton("Назад", callback_data='view_back'))
            await query.message.answer('Выберите экзамен для дальнейших действий. Или вернитесь назад.', reply_markup=markup)
        else:
            markup.insert(types.InlineKeyboardButton("Назад", callback_data='view_back'))
            await query.message.answer('Записей не обнаружено. Вернитесь назад.', reply_markup=markup)



    if "back" in query.data:
        await les_menu(query.message)

            
            
        
async def edit_works(query: types.CallbackQuery):

    if "ex" in query.data:
        lesson_type, date, name_inspector, id_exam = query.data.split('_')[2:]
        markup = types.InlineKeyboardMarkup(row_width=1)
        rules = 'Вы не можете отменить эту запись.'
        if datetime.date.today().strftime('%Y-%m-%d') < date:
            rules = 'Вы можете отменить эту запись.'
            markup.insert(types.InlineKeyboardButton(text="Отменить запись", callback_data=f"return_exam_{id_exam}"))
        markup.insert(types.InlineKeyboardButton(text="Назад", callback_data="view_back"))

        if lesson_type == '3':
            msg = f'Ваша запись:\nТеоретический экзамен\nДата {date}\n\nИнспектор:\n{name_inspector}\n\nМесто занятия:\nМРЭО ГИБДД \n\n\n {rules}'
        elif lesson_type == '4':
            msg = f'Ваша запись:\nПрактический экзамен\nДата {date}\n\nИнспектор:\n{name_inspector}\n\nМесто занятия:\nУточняйте по телефону. \n\n\n {rules}'
    else:
        date, time, id_teacher, id_class, lesson_type, id_practic = query.data.split('_')[1:]
        markup = types.InlineKeyboardMarkup(row_width=1)
        rules = 'Вы не можете отменить эту запись.'
        if lesson_type == '1':
            info_teacher, info_class = db.get_ihfoles(id_teacher, id_class)
            if datetime.date.today().strftime('%Y-%m-%d') < date:
                rules = 'Вы можете отменить эту запись.'
                markup.insert(types.InlineKeyboardButton(text="Отменить занятие", callback_data=f"return_lesson_{id_practic}"))
            msg = f'Ваше занятие:\nПрактическое занятие\nДата {date}      Время {time} \n\nИнструктор:\n{info_teacher[0]}\nТелефон:   +{info_teacher[1]}\nemail:   {info_teacher[2]} \n\n Место занятия:\n{info_class[0]} {info_class[1]} \n\n\n {rules}'
        elif lesson_type == '2':
            info_teacher, info_class = db.get_ihfoles(id_teacher, id_class)
            msg = f'Ваше занятие:\nТеоретическое занятие\nДата {date}      Время {time} \n\nИнструктор:\n{info_teacher[0]}\nТелефон:   +{info_teacher[1]}\nemail:   {info_teacher[2]} \n\n Место занятия:\n{info_class[0]} каб.{info_class[1]} \n\n\n {rules}'
        markup.insert(types.InlineKeyboardButton(text="Назад", callback_data="view_back"))
    await query.message.answer(msg, reply_markup=markup)
    

            

async def return_works(query: types.CallbackQuery):

    if "exam" in query.data:
        db.del_exam(query.data.split('_')[-1])
        await query.answer(text="Запись успешно отменена.",show_alert=True)
        await les_menu(query.message)



    
    if "lesson" in query.data:
        db.del_lesson(query.data.split('_')[-1])
        db.update_balance(query.from_user.id, 500)
        number = random.randint(1, 1000)
        data = db.get_full_data(query.from_user.id)
        now = datetime.datetime.now()
        try:

            Generate_invoice("test.html",f'invoice_return{number}{query.from_user.id}.html',number, data[2], query.from_user.id,
                      data[5], "000012345",data[1],'4 цифры карты', f'{now.date()} {now.time()}', 'Возврат', 
                      'Возврат за занятие.', 500, "Возврат", data[8] )
        except:
            print(f"Чек номер {number} не создан. Ошибка!")


    
        try:
            Convert_and_send(f'invoice_return{number}{query.from_user.id}.html', f'invoice_return{number}{query.from_user.id}.pdf',data[5] )

        
        except:
            print(f"Чек номер {number} не отправлен. Ошибка!")


        await query.answer(text="Занятие успешно отменено. Деньги вернуться на Ваш баланс.",show_alert=True)
        await les_menu(query.message)








        

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(les_menu, lambda message: message.text == "📅 Управление расписанием" )
    dp.register_callback_query_handler(view_works, lambda query: query.data.startswith('view_'))
    dp.register_callback_query_handler(edit_works, lambda query: query.data.startswith('work_'))
    dp.register_callback_query_handler(return_works, lambda query: query.data.startswith('return_'))
