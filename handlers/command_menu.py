import random
from invoice.generate_send import Generate_invoice, Convert_and_send
from db import Database
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp,bot,db
import datetime
async def teacher_menu(message: types.Message,id = 0):
    await bot.delete_message(message.chat.id, message.message_id)
    id_teacher = db.check_rules_teacher(message.from_user.id) if id ==0 else db.check_rules_teacher(id)
    if id_teacher is None:
        await message.answer(text="У вас нет доступа к этому разделу",show_alert=True)
    else:
        

        keyboard_rec = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Мои данные", callback_data=f"teach_data_{id_teacher}")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
        b2 = types.InlineKeyboardButton(text="Расписание на день", callback_data=f"teach_table_{id_teacher}")
        b3 = types.InlineKeyboardButton(text="Отменить занятие", callback_data=f"teach_ret_lesson_{id_teacher}")
        b4= types.InlineKeyboardButton(text="Отметить ученика", callback_data=f"teach_true_lesson_{id_teacher}")
        #b5= types.InlineKeyboardButton(text="Ошибки", callback_data="mode_errors")

        b6 = types.InlineKeyboardButton(text="Меню", callback_data="menu")


        keyboard_rec.add(b1,b2,b3,b4,b6) 

        #PR сюда нужно ценую занятия.
        await message.answer('Вы перешли в меню преподавателя! Выберите интересующий раздел?.', reply_markup=keyboard_rec)#reply_markup=types.ReplyKeyboardRemove()



async def teacher_mode(query: types.CallbackQuery):
    
    
    if "data" in query.data:
        await query.message.delete()
        lst_full_data = db.get_full_teacher_data(query.from_user.id)
        keyboard_rec = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Назад", callback_data=f"teach_back_{query.from_user.id}")
        keyboard_rec.add(b1) 
        await query.message.answer(
                f'Ваши данные:\n'
                f'Логин {lst_full_data[1]}\n'
                f'Имя {lst_full_data[3]}\n'
                f'Телефон +{lst_full_data[2]}\n'
                f'Дата рождения {lst_full_data[4]}\n'
                f'Опыт работы {lst_full_data[5]} лет\n'
                f'Электронный адрес {lst_full_data[6]}\n\n'
                f'Данные о машине:\n'
                f'Коробка передач {lst_full_data[7]}\n'
                f'Марка {lst_full_data[8]}\n'
                f'Цвет {lst_full_data[9]}\n'
                f'Номер {lst_full_data[10]}\n',
                reply_markup=keyboard_rec
)
        
    if "table" in query.data:
        await query.message.delete()
        lessons_lst = db.get_lessons_days(query.data.split('_')[-1],datetime.date.today())
        markup = types.InlineKeyboardMarkup(row_width=1)
        if len(lessons_lst)!=0:
            
            lessons_lst = sorted(lessons_lst, key=lambda x: x[0])
            for i in range(len(lessons_lst)):
                if i <=3:
                    callback = f"tach-les_view_{lessons_lst[i][0]}_{query.data.split('_')[-1]}" 
                    
                    text = f"Занятия {lessons_lst[i][0]}"
                    markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
                else:
                    pass
            markup.insert(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Выберите день занятий для дальнейших действий. Или вернитесь назад. \n\nВам доступно 4 ближайших дня с занятиями. ', reply_markup=markup)
        else:
            markup.insert(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Занятий не обнаружено. Вернитесь назад.', reply_markup=markup)

    if "ret_lesson" in query.data:
        await query.message.delete()
        lessons_lst = db.get_lessons_days(query.data.split('_')[-1],datetime.date.today())
        markup = types.InlineKeyboardMarkup(row_width=1)
        if len(lessons_lst)!=0:
            
            lessons_lst = sorted(lessons_lst, key=lambda x: x[0])
            for i in range(len(lessons_lst)):
                if i <=6:
                    callback = f"tach-les_return_{lessons_lst[i][0]}_{query.data.split('_')[-1]}" 
                    
                    text = f"Занятия {lessons_lst[i][0]}"
                    markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
                else:
                    pass
            markup.insert(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Выберите день занятий для дальнейших действий. Или вернитесь назад. \n\nВам доступно 7 ближайших дней с занятиями. ', reply_markup=markup)
        else:
            markup.insert(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Занятий не обнаружено. Вернитесь назад.', reply_markup=markup)
    if "true_lesson" in query.data:
        await query.message.delete()
        lessons_lst = db.get_lessons_days(query.data.split('_')[-1],datetime.date.today(),True)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if len(lessons_lst)!=0:
            
            lessons_lst = sorted(lessons_lst, key=lambda x: x[0], reverse=True)
            for i in range(len(lessons_lst)):
                if i <=6:
                    callback = f"tach-les_rul_{lessons_lst[i][0]}_{query.data.split('_')[-1]}" 
                    
                    text = f"Занятия {lessons_lst[i][0]}"
                    markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
                else:
                    pass
            markup.insert(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Выберите день занятий для дальнейших действий. Или вернитесь назад. \n\nВам доступно 7 ближайших дней с занятиями. ', reply_markup=markup)
        else:
            markup.insert(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Занятий не обнаружено. Вернитесь назад.', reply_markup=markup)

    if "back" in query.data:
        await teacher_menu(query.message,query.data.split('_')[-1])
       
async def get_lessons_day(query: types.CallbackQuery):
    if "return" in query.data:
        await query.message.delete()
        teacher_id=query.data.split('_')[-1]
        date = query.data.split('_')[-2]
        lessons_lst = db.get_lesson_on_day(query.data.split('_')[-1],query.data.split('_')[-2])
        markup = types.InlineKeyboardMarkup(row_width=2)
        if len(lessons_lst)!=0:
            
            lessons_lst = sorted(lessons_lst, key=lambda x: x[2])
            for i in range(len(lessons_lst)):
                callback = f"t-return_{lessons_lst[i][0]}" 
                text = f"{lessons_lst[i][2]}"
                markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
            markup.add(types.InlineKeyboardButton("Отменить все", callback_data=f't-return_all_{date}_{teacher_id}'))    
            markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Выберите время для отмены или отменить все. Также можете вернуться назад.', reply_markup=markup)
        else:
            markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Занятий не обнаружено. Вернитесь назад.', reply_markup=markup)
    if "view" in query.data:
        await query.message.delete()
        teacher_id=query.data.split('_')[-1]
        date = query.data.split('_')[-2]
        lessons_lst = db.get_lesson_on_day(query.data.split('_')[-1],query.data.split('_')[-2])
        markup = types.InlineKeyboardMarkup(row_width=2)
        if len(lessons_lst)!=0:
            
            lessons_lst = sorted(lessons_lst, key=lambda x: x[2])
            for i in range(len(lessons_lst)):
                callback = f"t-view_{lessons_lst[i][0]}" 
                text = f"{lessons_lst[i][2]}"
                markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
            markup.add(types.InlineKeyboardButton("Запросить подробное расписание на почту", callback_data=f't-view_all_{date}_{teacher_id}'))    
            markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Выберите время чтобы посмотреть подробнее. Также можете вернуться назад.', reply_markup=markup)
        else:
            markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Занятий не обнаружено. Вернитесь назад.', reply_markup=markup)
    if "rul" in query.data:
        await query.message.delete()
        teacher_id=query.data.split('_')[-1]
        date = query.data.split('_')[-2]
        lessons_lst = db.get_lesson_on_day(query.data.split('_')[-1],query.data.split('_')[-2])
        markup = types.InlineKeyboardMarkup(row_width=2)
        if len(lessons_lst)!=0:
            
            lessons_lst = sorted(lessons_lst, key=lambda x: x[2])
            for i in range(len(lessons_lst)):
                callback = f"t-rul_{lessons_lst[i][0]}" 
                text = f"{lessons_lst[i][2]}"
                markup.insert(types.InlineKeyboardButton(text, callback_data=callback))
            markup.add(types.InlineKeyboardButton("Отметить всех", callback_data=f't-rul_all_{date}_{teacher_id}'))    
            markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Выберите время чтобы отметить ученика. Также можете вернуться назад.', reply_markup=markup)
        else:
            markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
            await query.message.answer('Занятий не обнаружено. Вернитесь назад.', reply_markup=markup)


async def rules_mode(query: types.CallbackQuery):
    if "all" in query.data: 
        await query.message.delete()
        
        lessons = db.get_lesson_on_day(query.data.split('_')[-1],query.data.split('_')[-2])
        for i in range(len(lessons)):
            db.update_count_lesson(lessons[i][-1])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("Выйти", callback_data=f'teach_back_{query.from_user.id}'))
        await query.message.answer('Ученики отмечены. Спасибо!', reply_markup=markup)
    else:
        await query.message.delete()
        info = db.get_info_lesson(query.data.split('_')[-1])
        db.update_count_lesson(info[-1])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("Выйти", callback_data=f'teach_back_{query.from_user.id}'))
        await query.message.answer('Ученик отмечен. Спасибо!', reply_markup=markup)
        

async def view_mode(query: types.CallbackQuery):
    if "all" in query.data: #PR сюда нужно html расписание
        await query.message.delete()
        pass
    else:
        await query.message.delete()
        info = db.get_info_lesson(query.data.split('_')[-1])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("Выйти", callback_data=f'teach_back_{query.from_user.id}'))
        await query.message.answer(f'Информация о занятии:\nЗанятие {info[0]} {info[1]}\n\nКандидат в водители:\nИмя {info[2]}\nНомер телефона +{info[3]}\nemail {info[4]}\n\nМесто встречи {info[5]} {info[6]}', reply_markup=markup)
        


async def return_mode(query: types.CallbackQuery):
    if "all" in query.data:
        await query.message.delete()
        lessons = db.get_lesson_on_day(query.data.split('_')[-1],query.data.split('_')[-2])
        db.del_lesson_on_day(query.data.split('_')[-1],query.data.split('_')[-2])
        for i in range(len(lessons)):
            db.update_balance(lessons[i][-1], 500,True)
            number = random.randint(1, 1000)
            data = db.get_full_data(lessons[i][-1],True)
            now = datetime.datetime.now()
            try:
                Generate_invoice("test.html",f'invoice_return{number}{data[0]}.html',number, data[2], data[0],
                        data[5], "000012345",data[1],'4 цифры карты', f'{now.date()} {now.time()}', 'Возврат', 
                        'Отмена занятия инструктором.', 500, "Возврат", data[8] )
            except:
                print(f"Чек номер {number} не создан. Ошибка!")

            try:
                Convert_and_send(f'invoice_return{number}{data[0]}.html', f'invoice_return{number}{data[0]}.pdf',data[5] )
            except:
                print(f"Чек номер {number} не отправлен. Ошибка!")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
        await query.message.answer(f"Занятия на {query.data.split('_')[-2]} успешно отменены ", reply_markup=markup)
        
    else:
        await query.message.delete()
        id_student = db.del_lesson(query.data.split('_')[-1],True)
        db.update_balance(id_student, 500,True)
        number = random.randint(1, 1000)
        data = db.get_full_data(id_student,True)
        now = datetime.datetime.now()
        try:
            Generate_invoice("test.html",f'invoice_return{number}{data[0]}.html',number, data[2], data[0],
                    data[5], "000012345",data[1],'4 цифры карты', f'{now.date()} {now.time()}', 'Возврат', 
                    'Отмена занятия инструктором.', 500, "Возврат", data[8] )
        except:
            print(f"Чек номер {number} не создан. Ошибка!")
        try:
            Convert_and_send(f'invoice_return{number}{data[0]}.html', f'invoice_return{number}{data[0]}.pdf',data[5] )
        except:
            print(f"Чек номер {number} не отправлен. Ошибка!")
            
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("Назад", callback_data=f'teach_back_{query.from_user.id}'))
        await query.message.answer("Занятие успешно отменено ", reply_markup=markup)
        

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(teacher_menu, commands=['teacher'] )
    dp.register_callback_query_handler(teacher_mode, lambda query: query.data.startswith('teach_'))
    dp.register_callback_query_handler(get_lessons_day, lambda query: query.data.startswith('tach-les'))
    dp.register_callback_query_handler(return_mode, lambda query: query.data.startswith('t-return'))
    dp.register_callback_query_handler(view_mode, lambda query: query.data.startswith('t-view'))
    dp.register_callback_query_handler(rules_mode, lambda query: query.data.startswith('t-rul'))

    # dp.register_message_handler(admin_menu, commands=['admin'] )
    
    