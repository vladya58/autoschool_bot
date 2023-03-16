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
    b2 = types.InlineKeyboardButton(text="Теор. экзамен", callback_data="t_exam")
    b3 = types.InlineKeyboardButton(text="Пр. экзамен", callback_data="p_exam")
    b4 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    

    keyboard_rec.add(b1,b2,b3,b4) 


    await message.answer('Вы перешли в меню записи! Выберите на что хотите записаться.', reply_markup=keyboard_rec)#reply_markup=types.ReplyKeyboardRemove()


async def rec(callback: types.CallbackQuery, state: FSMContext):
   
    if callback.data == "lesson":
        await callback.message.delete()
        await bot.answer_callback_query(callback.id)
        await show_calendar(callback.message.chat.id)


    elif callback.data == "t_exam":
        pass
    elif callback.data == "p_exam":
        pass
    elif callback.data == "back_to_rec":
        await rec_menu(callback.message)
        

async def show_calendar(chat_id: int):
    markup = create_calendar()
    await bot.send_message(chat_id, "Выберите дату", reply_markup=markup)

def create_calendar(year=None, month=None):
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    markup = types.InlineKeyboardMarkup(row_width=7)
    month_names = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                   "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")
    # Первая строка - месяц и год
    row = [types.InlineKeyboardButton("◀️", callback_data=f"calendar-prev-month-{year}-{month}"),
           types.InlineKeyboardButton(month_names[month - 1] + " " + str(year), callback_data="ignore"),
           types.InlineKeyboardButton("▶️", callback_data=f"calendar-next-month-{year}-{month}")]
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
                row.append(types.InlineKeyboardButton(str(day), callback_data=f"calendar-day-{month}-{day}"))
        markup.row(*row)
    return markup


async def calendar_prev_month_callback(query):
    year, month = map(int, query.data.split('-')[3:])
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  reply_markup=create_calendar(prev_year, prev_month))



async def calendar_next_month_callback(query):
    year, month = map(int, query.data.split('-')[3:])
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                        reply_markup=create_calendar(next_year, next_month))

async def show_time_picker(message_id: int, chat_id: int, selected_day: int,selected_month:int):
    await bot.delete_message(chat_id,message_id)
    # Показываем пользователю выбор времени
    now = datetime.datetime.now()
    markup = types.InlineKeyboardMarkup(row_width=2)
    for hour in range(8, 19):
        time_str = f"{hour:02}:00"
        callback_data = f"lesson-time-2023-{selected_month}-{selected_day}-{time_str}"
        button_text = time_str if datetime.datetime.strptime(callback_data, "lesson-time-%Y-%m-%d-%H:%M") > datetime.datetime.combine(now.date(), now.time()) else f"{time_str} (уже прошло)"
        callback_data = callback_data + " прошло" if "прошло" in button_text else callback_data  
        markup.insert(types.InlineKeyboardButton(button_text, callback_data=callback_data))
    await bot.send_message(chat_id, "Выберите время", reply_markup=markup)

async def process_lesson_callback(callback_data: types.CallbackQuery):
    if "прошло" in callback_data.data:
        keyboard = types.InlineKeyboardMarkup()
    
        b2 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_rec")
        selected_year_str,selected_month_str,selected_day_str, selected_time_str = callback_data.data.split('-')[2:]
        keyboard.add(b2) 
        await callback_data.message.delete()

        await callback_data.message.answer ('Вы выбрали дату которая прошла. Вернитесь назад!', reply_markup=keyboard)
    
    else:



        keyboard = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Записаться", callback_data="lesson_rec")
        b2 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_rec")
        selected_year_str,selected_month_str,selected_day_str, selected_time_str = callback_data.data.split('-')[2:]
        keyboard.add(b1,b2) 

        await callback_data.message.delete()

        await callback_data.message.answer (f'Ваша запись:Год {selected_year_str} День {selected_day_str},Месяц {selected_month_str}, Время {selected_time_str}', reply_markup=keyboard)
    
    

async def process_calendar_day(callback_query: types.CallbackQuery):
    selected_month,selected_day = callback_query.data.split('-')[2:]
   
    await show_time_picker(callback_query.message.message_id,callback_query.message.chat.id, selected_day,selected_month)


    





def register_handlers(dp: Dispatcher):
    dp.register_message_handler(rec_menu, lambda message: message.text == "🚘 Записаться на вождение" )
    dp.register_callback_query_handler(rec, lambda callback: callback.data in ["lesson","t_exam","p_exam","back_to_rec"] )
    
    dp.register_callback_query_handler(calendar_next_month_callback, lambda query: query.data.startswith('calendar-next-month'))
    dp.register_callback_query_handler(calendar_prev_month_callback, lambda query: query.data.startswith('calendar-prev-month'))

    dp.register_callback_query_handler(process_calendar_day, lambda c: c.data.startswith('calendar-day-'))
    dp.register_callback_query_handler(process_lesson_callback, lambda c: c.data.startswith('lesson-time-'))
   