import random
from invoice.generate_send import Generate_invoice, Convert_and_send
from db import Database
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp,bot,db
import datetime
from aiogram.dispatcher import FSMContext
import asyncio
from typing import Union
from aiogram.dispatcher.filters.state import State, StatesGroup

class LoginStates(StatesGroup):
    PASSWORD_STATE = State()

class DBStates(StatesGroup):
    newStudent = State()
    newGroup = State()
    newCategory = State()
    newProgram = State()
    newCar = State()
    newClass = State()
    newTeacher = State()

async def admin_sign(message: types.Message,state: FSMContext,id = 0):
    await bot.delete_message(message.chat.id, message.message_id)
    log_user= message.from_user.id if id ==0 else id
    
    with open('admin.txt', 'r') as file:
        admin_data = file.readlines()
        admin_log = int(admin_data[0].split('=')[1].strip())
        admin_pas = admin_data[1].split('=')[1].strip()

    if log_user == admin_log:

        await state.update_data(admin_pas=admin_pas)
        await message.answer("Введите пароль")
        await LoginStates.PASSWORD_STATE.set()
    else:
        await bot.send_message(message.chat.id, 'У вас нет доступа')
@dp.message_handler(state=LoginStates.PASSWORD_STATE)
async def password_handler(message: types.Message, state: FSMContext):
    # получаем сохраненный логин из user_data
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    data = await state.get_data()
    admin_pas = data.get("admin_pas")
    password = message.text
    await admin_menu(message)

    # проверяем пароль
    if password == admin_pas:
        await state.finish()
        
    else:
        await message.answer("Отказано в доступе.")
        


    
async def admin_menu(message: types.Message):
    keyboard_rec = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton(text="Студенты", callback_data=f"admin_student")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    b2 = types.InlineKeyboardButton(text="Группы", callback_data=f"admin_group")
    b3 = types.InlineKeyboardButton(text="Расписание", callback_data=f"admin_table") #не сделал
    b4 = types.InlineKeyboardButton(text="Категории", callback_data=f"admin_category")
    b5 = types.InlineKeyboardButton(text="Программы", callback_data=f"admin_programm")
    b6 = types.InlineKeyboardButton(text="Даты Экз.", callback_data=f"admin_exam")#не сделал
    b7 = types.InlineKeyboardButton(text="Машины", callback_data=f"admin_car")
    b8= types.InlineKeyboardButton(text="Классы", callback_data=f"admin_class")
    b9= types.InlineKeyboardButton(text="Учителя", callback_data=f"admin_teachers")
    b10= types.InlineKeyboardButton(text="Результаты", callback_data=f"admin_result")#не сделал
    keyboard_rec.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10) 
    await message.answer('Авторизация успешна! Выберите таблицу для изменения.', reply_markup=keyboard_rec)

async def admin_mode(query: types.CallbackQuery):

    options = {
    "student": {
        "Добавить студента": "adm_student_add",
        "Удалить студента": "adm_student_del",
        "Редактировать студента": "adm_student_edit"
    },
    "group": {
        "Добавить группу": "adm_group_add",
        "Удалить группу": "adm_group_del",
        "Редактировать группу": "adm_group_edit"
    },
    "category": {
        "Добавить категорию": "adm_category_add",
        "Удалить категорию": "adm_category_del",
        "Редактировать категорию": "adm_category_edit"
    },
    "programm": {
        "Добавить программу": "adm_programm_add",
        "Удалить программу": "adm_programm_del",
        "Редактировать программу": "adm_programm_edit"
    },
    "car": {
        "Добавить машину": "adm_car_add",
        "Удалить машину": "adm_car_del",
        "Редактировать машину": "adm_car_edit"
    },
    "class": {
        "Добавить класс": "adm_class_add",
        "Удалить класс": "adm_class_del",
        "Редактировать класс": "adm_class_edit"
    },
    "teachers": {
        "Добавить учителя": "adm_teachers_add",
        "Удалить учителя": "adm_teachers_del",
        "Редактировать учителя": "adm_teachers_edit"
    },
}

    for key, value in options.items():
        if key in query.data:
            await query.message.delete()
            markup = types.InlineKeyboardMarkup(row_width=1)
            for action, callback in value.items():
                markup.insert(types.InlineKeyboardButton(action, callback_data=callback))
            markup.insert(types.InlineKeyboardButton("Назад", callback_data=f'admin_back_{query.from_user.id}'))
            await query.message.answer('Что вы хотите сделать?', reply_markup=markup)
            
    if "back" in query.data:
            
            await query.message.delete()
            await admin_menu(query.message)
            
                




@dp.message_handler(state=DBStates.newProgram or DBStates.newGroup or DBStates.newStudent or DBStates.newCategory or DBStates.newCar or DBStates.newClass or DBStates.newTeacher )
async def add_mode(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    answer = message.text
    values = answer.split(',')
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.delete_message(message.chat.id, message.message_id)
    if 'newStudent' in current_state:
        await state.finish()
        try:
            db.add_user(str(values[0]),int(values[1]))
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            await message.answer('Студент добавлен!', reply_markup=keyboard_rec)
        except Exception as e:
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            print(f"Ошибка: {str(e)}")
            await message.answer('Что-то пошло не так. Ошибка', reply_markup=keyboard_rec) 
    elif 'newGroup' in current_state:
        await state.finish()
        try:
            db.add_group(int(values[0]), int(values[1]), int(values[2]))
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            await message.answer('Группа добавлена!', reply_markup=keyboard_rec)
        except Exception as e:
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            print(f"Ошибка: {str(e)}")
            await message.answer('Что-то пошло не так. Ошибка', reply_markup=keyboard_rec)
    elif 'newProgram' in current_state:
        await state.finish()
        try:
            db.add_programm(str(values[0]),float(values[1]),int(values[2]),int(values[3]),int(values[4]),int(values[5]))
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            await message.answer('Программа добавлена!', reply_markup=keyboard_rec)
        except Exception as e:
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            print(f"Ошибка: {str(e)}")
            await message.answer('Что-то пошло не так. Ошибка', reply_markup=keyboard_rec)
    elif 'newCategory' in current_state:
        await state.finish()
        try:
            db.add_category(str(values[0]))
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            await message.answer('Категория добавлена!', reply_markup=keyboard_rec)
        except Exception as e:
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            print(f"Ошибка: {str(e)}")
            await message.answer('Что-то пошло не так. Ошибка', reply_markup=keyboard_rec)
    elif 'newCar' in current_state:
        await state.finish()
        try:
            db.add_car(str(values[0]),str(values[1]),str(values[2]),str(values[3]),int(values[4]))
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            await message.answer('Машина добавлена!', reply_markup=keyboard_rec)
        except Exception as e:
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            print(f"Ошибка: {str(e)}")
            await message.answer('Что-то пошло не так. Ошибка', reply_markup=keyboard_rec)

    elif 'newClass' in current_state:
        await state.finish()
        try:
            db.add_class(str(values[0]),str(values[1]))
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            await message.answer('Класс добавлен!', reply_markup=keyboard_rec)
        except Exception as e:
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            print(f"Ошибка: {str(e)}")
            await message.answer('Что-то пошло не так. Ошибка', reply_markup=keyboard_rec)

    elif 'newTeacher' in current_state:
        await state.finish()
        try:
            db.add_teacher(int(values[0]),str(values[1]),str(values[2]),str(values[3]),float(values[4]),str(values[5]))
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            await message.answer('Учитель добавлен!', reply_markup=keyboard_rec)
        except Exception as e:
            keyboard_rec = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text="Выход", callback_data=f"admin_back_{message.from_user.id}")
            keyboard_rec.add(b1) 
            print(f"Ошибка: {str(e)}")
            await message.answer('Что-то пошло не так. Ошибка', reply_markup=keyboard_rec)

async def admin_option(query: types.CallbackQuery,state: FSMContext):   
    if "add" in query.data:
        await query.message.delete()
        if query.data.split('_')[-2] == "student":
            await query.message.answer('Введите через запятую значение номера телефона(без +) и группы. Пример "79999999999, 1"')
            await DBStates.newStudent.set()
        if query.data.split('_')[-2] == "group":
            await query.message.answer('Введите через запятую значения "Кол-во студентов, id учителя, id программы обучения". Пример "15, 1, 1"')
            await DBStates.newGroup.set()
        if query.data.split('_')[-2] == "category":
            await query.message.answer('Введите букву(ы) категории(без пробелов). Пример "AB"')
            await DBStates.newCategory.set()
        if query.data.split('_')[-2] == "programm":
            await query.message.answer('Введите через запятую значения "Название программы, стоимость практического занятия, кол-во практических занятий, кол-во теоретических занятий, id группы, id категории". Пример "Новая программа, 1000, 56, 65, 1, 1"')
            await DBStates.newProgram.set()
        if query.data.split('_')[-2] == "car":
            await query.message.answer('Введите через запятую значения "Вид КПП, марка, цвет, номер, id учителя". Пример "Механика, Лада Калина, Серая,  К124УУ58, 1"')
            await DBStates.newCar.set()
        if query.data.split('_')[-2] == "class":
            await query.message.answer('Введите через запятую значения "Адрес, уточнение". Пример "Пушкина 37, Магазин Пятерочка"')
            await DBStates.newClass.set()
        if query.data.split('_')[-2] == "teachers":
            await query.message.answer('Введите через запятую значения "Логин, Номер телефона (без +), ФИО, дата рождения, опыт преподавания, емаил". Пример "00000, 79636357830, Иванов Иван Иванович, 1900-05-28, 34, email@mail.ru"')
            await DBStates.newTeacher.set()




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
        keyboard_rec.add(b1,b2,b3,b4) 

        
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
    dp.register_message_handler(admin_sign, commands=['admin'] )
    dp.register_callback_query_handler(teacher_mode, lambda query: query.data.startswith('teach_'))
    dp.register_callback_query_handler(admin_mode, lambda query: query.data.startswith('admin_'))
    dp.register_callback_query_handler(get_lessons_day, lambda query: query.data.startswith('tach-les'))
    dp.register_callback_query_handler(admin_option, lambda query: query.data.startswith('adm_'))
    dp.register_callback_query_handler(return_mode, lambda query: query.data.startswith('t-return'))
    dp.register_callback_query_handler(view_mode, lambda query: query.data.startswith('t-view'))
    dp.register_callback_query_handler(rules_mode, lambda query: query.data.startswith('t-rul'))
    dp.register_message_handler(add_mode, state=[DBStates.newProgram, DBStates.newGroup, DBStates.newStudent, DBStates.newCategory, DBStates.newCar, DBStates.newClass, DBStates.newTeacher], content_types=types.ContentTypes.TEXT)

    # dp.register_message_handler(admin_menu, commands=['admin'] )
    
    