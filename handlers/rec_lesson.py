from create_bot import dp,bot,db
from db import Database
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
import calendar
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRec(StatesGroup):
    date = State()
    time = State()


#@dp.message_handler(lambda message: message.text == "🚘 Записаться на вождение")
async def rec_menu(message: types.Message):
    
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_rec = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Занятие", callback_data="lesson")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    b2 = types.InlineKeyboardButton(text="Теоретический экзамен", callback_data="t_exam")
    b3 = types.InlineKeyboardButton(text="Практический экзамен", callback_data="p_exam")
    b4 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    

    keyboard_rec.add(b1,b2,b3,b4) 


    await message.answer('Вы перешли в меню записи! Выберите на что хотите записаться.\n\n Помните, что запись на экзамены формируется только после прохождения всех теоретических и парктических занятий предусмотренных программой обучения.\n\nДни для экзамена формирует МРЭО ГИБДД самостоятельно, обычно 2 дня в неделю. Нажмите на нужный экзамен для просмотра этих дней. \n\n\nОплата экзаменов происходит в МРЭО ГИБДД. Не забудьте мед. справку, паспорт и сертификат об окончании Автошколы.', reply_markup=keyboard_rec)#reply_markup=types.ReplyKeyboardRemove()


async def rec(callback: types.CallbackQuery, state: FSMContext):
    lesson = False
    t_exam = False
    p_exam = False
   
    if callback.data == "lesson":
        lesson = True
        await callback.message.delete()
        await bot.answer_callback_query(callback.id)
        await show_calendar(lesson, t_exam, p_exam, callback.message.chat.id)


    elif callback.data == "t_exam":
        t_exam = True
        await callback.message.delete()
        await bot.answer_callback_query(callback.id)
        await exams(lesson, t_exam, p_exam, callback.message.chat.id)
        
    elif callback.data == "p_exam":
        p_exam = True
        await callback.message.delete()
        await bot.answer_callback_query(callback.id)
        await exams(lesson, t_exam, p_exam, callback.message.chat.id)
        
    elif callback.data == "back_to_rec":
        await rec_menu(callback.message)
        


async def exams(lesson, t_exam, p_exam,chat_id: int):
    if t_exam:
        date_array = db.show_date_exam(3, datetime.date.today())                   
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in range(len(date_array)):
            count_st = db.show_count_slots(date_array[i][0])
            date_str = date_array[i][1].strftime("%Y-%m-%d")
            callback_data = f"rec- t_exam -{date_str}"
            button_text = f"{date_str}, Осталось {date_array[i][2]-len(count_st)} из {date_array[i][2]} мест"
            markup.insert(types.InlineKeyboardButton(button_text, callback_data=callback_data))

        markup.insert(types.InlineKeyboardButton("Назад", callback_data="back_to_rec"))
        await bot.send_message(chat_id, "Выберите день теорeтического экзамена. Нажимая на выбранный день, вы подтверждаете свою запись на этот день. Отменить эту запись можно будет в главном меню.", reply_markup=markup)
    if p_exam:
        date_array = db.show_date_exam(4, datetime.date.today())                   
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in range(len(date_array)):
            count_st = db.show_count_slots(date_array[i][0])
            date_str = date_array[i][1].strftime("%Y-%m-%d")
            callback_data = f"rec- p_exam -{date_str}"
            button_text = f"{date_str}, Осталось {date_array[i][2]-len(count_st)} из {date_array[i][2]} мест"
            markup.insert(types.InlineKeyboardButton(button_text, callback_data=callback_data))

        markup.insert(types.InlineKeyboardButton("Назад", callback_data="back_to_rec"))
        await bot.send_message(chat_id, "Выберите день практического экзамена. Нажимая на выбранный день, вы подтверждаете свою запись на этот день. Отменить эту запись можно будет в главном меню.", reply_markup=markup)
    

async def show_calendar(lesson, t_exam, p_exam,chat_id: int):
    markup = create_calendar(lesson, t_exam, p_exam)
    await bot.send_message(chat_id, "Выберите дату", reply_markup=markup)

def create_calendar(lesson, t_exam, p_exam, year=None, month=None):
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    markup = types.InlineKeyboardMarkup(row_width=7)
    month_names = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                   "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")
    # Первая строка - месяц и год
    row = [types.InlineKeyboardButton("◀️", callback_data=f"calendar-prev-month-{year}-{month}-{lesson}-{t_exam}-{p_exam}"),
           types.InlineKeyboardButton(month_names[month - 1] + " " + str(year), callback_data="ignore"),
           types.InlineKeyboardButton("▶️", callback_data=f"calendar-next-month-{year}-{month}-{lesson}-{t_exam}-{p_exam}")]
    markup.row(*row)
    # Вторая строка - дни недели
    week_days = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
    row = [types.InlineKeyboardButton(day, callback_data="ignore") for day in week_days]
    markup.row(*row)
    # Остальные строки - дни месяца
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                
                row.append(types.InlineKeyboardButton(str(day), callback_data=f"calendar-day lesson -{month}-{day}"))
                
        
        markup.row(*row)
    return markup


async def calendar_prev_month_callback(query):
    lesson, t_exam, p_exam = query.data.split('-')[5:8]
    year, month = map(int, query.data.split('-')[3:5])
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  reply_markup=create_calendar(lesson, t_exam, p_exam,prev_year, prev_month))



async def calendar_next_month_callback(query):
    lesson, t_exam, p_exam = query.data.split('-')[5:8]
    year, month = map(int, query.data.split('-')[3:5])
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                        reply_markup=create_calendar(lesson, t_exam, p_exam,next_year, next_month))

async def show_time_picker(user_id: int, message_id: int, chat_id: int, selected_day: int,selected_month:int):
    await bot.delete_message(chat_id,message_id)
    time_array = db.check_table(user_id, selected_month,selected_day)
    for i in range(len(time_array)):
        time_array[i] = time_array[i][0].strftime("%H:%M")
    # Показываем пользователю выбор времени
    now = datetime.datetime.now()
    markup = types.InlineKeyboardMarkup(row_width=2)
    for hour in range(8, 19):
        if hour != 12:
            time_str = f"{hour:02}:00"
            callback_data = f"lesson-time-2023-{selected_month}-{selected_day}-{time_str}"
            if time_str not in time_array and datetime.datetime.strptime(callback_data, "lesson-time-%Y-%m-%d-%H:%M") > datetime.datetime.combine(now.date(), now.time()) and datetime.datetime.strptime(callback_data, "lesson-time-%Y-%m-%d-%H:%M").weekday() in [1,2,3,4]:
                button_text = time_str
                markup.insert(types.InlineKeyboardButton(button_text, callback_data=callback_data))
            else:
                button_text = time_str
                button_text = f"{time_str} (занято)" if time_str in time_array else button_text
                button_text = f"{time_str} (уже прошло)" if datetime.datetime.strptime(callback_data, "lesson-time-%Y-%m-%d-%H:%M") < datetime.datetime.combine(now.date(), now.time()) else button_text
                button_text = f"{time_str} (выходной)" if datetime.datetime.strptime(callback_data, "lesson-time-%Y-%m-%d-%H:%M").weekday() in [5,6] else button_text
            
                callback_data = callback_data + " занято" if "(занято)" in button_text else callback_data
                callback_data = callback_data + " выходной" if "(выходной)" in button_text else callback_data
                callback_data = callback_data + " прошло" if "прошло" in button_text else callback_data  
                markup.insert(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        else:
            pass
    markup.insert(types.InlineKeyboardButton("Назад", callback_data="back_to_rec"))
    await bot.send_message(chat_id, "Выберите время", reply_markup=markup)

async def process_lesson_callback(callback_data: types.CallbackQuery):
    if "прошло" in callback_data.data:
        keyboard = types.InlineKeyboardMarkup()
    
        b2 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_rec")
        selected_year_str,selected_month_str,selected_day_str, selected_time_str = callback_data.data.split('-')[2:]
        keyboard.add(b2) 
        await callback_data.message.delete()

        await callback_data.message.answer ('Вы выбрали дату которая прошла. Вернитесь назад!', reply_markup=keyboard)
    if "выходной" in  callback_data.data:
        keyboard = types.InlineKeyboardMarkup()
    
        b2 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_rec")
        selected_year_str,selected_month_str,selected_day_str, selected_time_str = callback_data.data.split('-')[2:]
        keyboard.add(b2) 
        await callback_data.message.delete()

        await callback_data.message.answer ('Вы выбрали выходной день. Вернитесь назад!', reply_markup=keyboard)
    
    if "занято" in callback_data.data:
        keyboard = types.InlineKeyboardMarkup()
    
        b2 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_rec")
        selected_year_str,selected_month_str,selected_day_str, selected_time_str = callback_data.data.split('-')[2:]
        keyboard.add(b2) 
        await callback_data.message.delete()

        await callback_data.message.answer ('Эти дата и время уже заняты. Вернитесь назад!', reply_markup=keyboard)

    else:


        selected_year_str,selected_month_str,selected_day_str, selected_time_str = callback_data.data.split('-')[2:]
        keyboard = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Записаться", callback_data=f"rec- lesson -{selected_year_str}-{selected_month_str}-{selected_day_str}-{selected_time_str}")
        b2 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_rec")
        
        keyboard.add(b1,b2) 

        await callback_data.message.delete()

        await callback_data.message.answer (f'Ваша запись:Год {selected_year_str} День {selected_day_str},Месяц {selected_month_str}, Время {selected_time_str}', reply_markup=keyboard)
    


async def process_calendar_day(callback_query: types.CallbackQuery):
    selected_month,selected_day = callback_query.data.split('-')[2:]
    await show_time_picker(callback_query.from_user.id,callback_query.message.message_id,callback_query.message.chat.id, selected_day,selected_month)
    
    

async def recover(callback_query: types.CallbackQuery):
    if "lesson" in callback_query.data:
        selected_year_str,selected_month_str,selected_day_str, selected_time_str = callback_query.data.split('-')[2:]
        db.rec_lesson(callback_query.from_user.id, f"{selected_year_str}-{selected_month_str}-{selected_day_str}",f"{selected_time_str}")
        await callback_query.answer(text="Запись на занятие прошла успешно!")
        await rec_menu(callback_query.message)    
    if "t_exam" in callback_query.data:
        selected_year_str,selected_month_str,selected_day_str = callback_query.data.split('-')[2:]
        try:
            db.rec_exam( callback_query.from_user.id,f"{selected_year_str}-{selected_month_str}-{selected_day_str}", 3)
            await callback_query.answer(text="Запись на теоретический экзамен прошла успешно!")
            await rec_menu(callback_query.message)       
        except:
            await callback_query.answer(text="Записаться не удалось. Возможно вы не прошли все занятия или уже были записаны на эту дату. Вы будете возращены в меню записи.",show_alert=True)
            await rec_menu(callback_query.message)

    if "p_exam" in callback_query.data:
        selected_year_str,selected_month_str,selected_day_str = callback_query.data.split('-')[2:]
        try:

            db.rec_exam( callback_query.from_user.id,f"{selected_year_str}-{selected_month_str}-{selected_day_str}", 4)
            await callback_query.answer(text="Запись на практический экзамен прошла успешно!")
            await rec_menu(callback_query.message)
        
        except:
            await callback_query.answer(text="Записаться не удалось. Возможно вы не прошли все занятия или уже были записаны на эту дату. Вы будете возращены в меню записи.",show_alert=True)
            await rec_menu(callback_query.message)
        
        

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(rec_menu, lambda message: message.text == "🚘 Записаться на вождение" )
    dp.register_callback_query_handler(rec, lambda callback: callback.data in ["lesson","t_exam","p_exam","back_to_rec"] )
    dp.register_callback_query_handler(recover, lambda query: query.data.startswith('rec'))
    
    dp.register_callback_query_handler(calendar_next_month_callback, lambda query: query.data.startswith('calendar-next-month'))
    dp.register_callback_query_handler(calendar_prev_month_callback, lambda query: query.data.startswith('calendar-prev-month'))

    dp.register_callback_query_handler(process_calendar_day, lambda c: c.data.startswith('calendar-day'))
    dp.register_callback_query_handler(process_lesson_callback, lambda c: c.data.startswith('lesson-time-'))
   