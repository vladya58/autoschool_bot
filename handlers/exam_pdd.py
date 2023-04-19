from create_bot import dp,bot,db
from db import Database
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import datetime
import calendar
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from invoice.generate_send import Generate_invoice, Convert_and_send
import os
from aiogram.utils.markdown import hspoiler
import random



async def menu_exam(message: types.Message):

    await bot.delete_message(message.chat.id, message.message_id-1) if message.text == "✅ Пройти экзамен ПДД" else None
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_rec = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Билеты", callback_data="mode_bilets")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    b2 = types.InlineKeyboardButton(text="Категории", callback_data="mode_category")
    b3 = types.InlineKeyboardButton(text="Самые сложные", callback_data="mode_hard")
    b4= types.InlineKeyboardButton(text="Экзамен", callback_data="mode_exam")
    b5= types.InlineKeyboardButton(text="Ошибки", callback_data="mode_errors")

    

    keyboard_rec.add(b1,b2,b3,b4,b5) 

    #PR сюда нужно ценую занятия.
    await message.answer('Вы перешли в меню тестирования! Выберите режим теста.\n\nЧтобы выйти в главное меню введите команду /menu или нажмите на нее!', reply_markup=keyboard_rec)#reply_markup=types.ReplyKeyboardRemove()

async def mode_quiz(query: types.CallbackQuery):
    
    
    if "exam" in query.data:
        await query.message.delete()
        blocks = {1: [], 2: [], 3: [], 4: []}
        for i in range(1, 801, 20):
            for k in range(1, 21):
                block_num = (k - 1) // 5 + 1
                blocks[block_num].append(k + i - 1)
        exam = []
        
        for block in blocks.values():
            exam += random.sample(block, 5)
        questions = db.get_answer_exam(exam)
        questions = sorted(questions, key=lambda x: x[-1])
        id_quiz = db.start_quiz(query.from_user.id,datetime.datetime.now().time(),"Экзамен")
        my_string = ", ".join(str(x[-1]) for x in questions)
        db.set_questions_quiz(my_string,id_quiz)

        question_index = 0
        await send_question(query.message.chat.id, question_index,questions, id_quiz,1) 

    if "bilets" in query.data:
        await query.message.delete()
        markup = types.InlineKeyboardMarkup(row_width=8) # Указываем row_width=8, чтобы поместить 8 кнопок в строку

        for i in range(1, 41):
            callback_data = f"bilet_{i}" # Присваиваем каждой кнопке уникальный callback_data
            button_text = str(i) # Устанавливаем текст кнопки, равный ее номеру
            button = types.InlineKeyboardButton(button_text, callback_data=callback_data)
            markup.insert(button)
        markup.add(types.InlineKeyboardButton("Назад", callback_data="mode_back"))
        await query.message.answer('Выберите номер билета или вернитесь назад', reply_markup=markup)

    if "hard" in query.data:
        await query.message.delete()
        # получаем все вопросы теста из базы данных
        answers = db.get_answers_hard()
        answers = sorted(answers, key=lambda x: x[-1])
        id_quiz = db.start_quiz(query.from_user.id,datetime.datetime.now().time(),"Сложные вопросы")
        my_string = ", ".join(str(x[-1]) for x in answers)
        db.set_questions_quiz(my_string,id_quiz)
        # начальный индекс вопроса
        question_index = 0
        await send_question(query.message.chat.id, question_index,answers, id_quiz)  
      
    if "category" in query.data:
        await query.message.delete()
        await show_category(query.message.chat.id)
            
    if "errors" in query.data:
        await query.message.delete()
        lst = db.get_qustions_error(query.from_user.id)
        if lst is None:
            markup = types.InlineKeyboardMarkup(row_width=1) # Указываем row_width=8, чтобы поместить 8 кнопок в строку
            markup.add(types.InlineKeyboardButton("Назад", callback_data="mode_back"))
            await query.message.answer('В вашем последнем пройденном тесте не было ошибок. Вернитесь назад.', reply_markup=markup)
        else:
            id_quiz = db.start_quiz(query.from_user.id,datetime.datetime.now().time(),"Просмотр ошибок")
            db.set_questions_quiz(lst,id_quiz)
            questions = db.get_answer_exam(lst.split(", ")[:-1])

            question_index = 0
            
            await send_question(query.message.chat.id, question_index,questions, id_quiz,2) 


    if "back" in query.data:
        await menu_exam(query.message)
    







async def bilet_mode(query: types.CallbackQuery):
    await query.message.delete()
    # получаем все вопросы теста из базы данных
    answers = db.get_answers_bilet(query.data.split('_')[-1])
    answers = sorted(answers, key=lambda x: x[-1])
    id_quiz = db.start_quiz(query.from_user.id,datetime.datetime.now().time(),f"Билет {query.data.split('_')[-1]}")
    my_string = ", ".join(str(x[-1]) for x in answers)
    db.set_questions_quiz(my_string,id_quiz)
    # начальный индекс вопроса
    question_index = 0
    bilet_number = query.data.split('_')[-1]
    bilet_number = 100 + int(bilet_number)
    # отправляем первый вопрос
    await send_question(query.message.chat.id, question_index,answers, id_quiz)   

async def category_mode(query: types.CallbackQuery):
    await query.message.delete()
    category = [    "Безопасность движения и техника управления автомобилем",    "Буксировка механических транспортных средств",    "Движение в жилых зонах",    "Движение по автомагистралям",    "Движение через железнодорожные пути",    "Дорожная разметка",    "Дорожные знаки",    "Начало движения маневрирование",    "Неисправности и условия допуска транспортных средств к эксплуатации",    "Обгон опережение встречный разъезд",    "Общие обязанности водителей",    "Общие положения",    "Оказание доврачебной медицинской помощи",    "Остановка и стоянка",    "Ответственность водителя",    "Перевозка людей и грузов",    "Пешеходные переходы и места остановок маршрутных транспортных средств",    "Пользование внешними световыми приборами и звуковыми сигналами",    "Применение аварийной сигнализации и знака аварийной остановки",    "Применение специальных сигналов",    "Приоритет маршрутных транспортных средств",    "Проезд перекрестков",    "Расположение транспортных средств на проезжей части",    "Сигналы светофора и регулировщика",    "Скорость движения",    "Учебная езда и дополнительные требования к движению велосипедистов"]
    # получаем все вопросы теста из базы данных
    index = query.data.split('_')[-1]
    index = int(index)
    answers = db.get_answers_category(category[index])
    answers = sorted(answers, key=lambda x: x[-1])

    id_quiz = db.start_quiz(query.from_user.id,datetime.datetime.now().time(),f"Категория {category[index]}")
    my_string = ", ".join(str(x[-1]) for x in answers)
    db.set_questions_quiz(my_string,id_quiz)
    # начальный индекс вопроса
    question_index = 0
    
    # отправляем первый вопрос
    await send_question(query.message.chat.id, question_index,answers, id_quiz)



async def send_question(chat_id, question_index, answers, id_quiz, annotation =0):
    # получаем информацию о текущем вопросе из списка ответов

    array = db.get_qustions(id_quiz)
    my_list = array[0].split(", ")
    answers = db.get_answer_exam((my_list[question_index],))

    current_question = answers[0]
    # формируем сообщение с текстом вопроса и вариантами ответов
    
    quest, *text_answ = map(str.strip, current_question[3].split('\n'))
    text_answ = '\n'.join(text_answ).strip()
    
    if annotation == 0:

        hidden_text = hspoiler(f"{current_question[4]}")
        question_message = f"<b>{quest}</b>\n{text_answ}\n\nПодсказка:\n{hidden_text}"
    elif annotation == 1:
        question_message = f"<b>{quest}</b>\n{text_answ}"
    elif annotation == 2:
        hidden_text = hspoiler(f"{current_question[4]}")
        hidden_text1 = hspoiler(f"Вариант ответа {current_question[2]}")
        question_message = f"<b>{quest}</b>\n{text_answ}\n\nПодсказка:\n{hidden_text}\nОтвет:\n{hidden_text1}"

    # если есть картинка, добавляем ее к сообщению
    if current_question[0] != "None":
        
        message = await bot.send_photo(chat_id, photo=open(f'{current_question[0]}', 'rb'), caption=question_message,parse_mode='HTML')
    else:
        message = await bot.send_message(chat_id, question_message,parse_mode='HTML')
    # сохраняем правильный ответ
    correct_answer = current_question[2]
    keyboard_markup = types.InlineKeyboardMarkup()
    for i in range(current_question[1]):
        callback_data = f"answer_{i + 1}_{correct_answer}_{question_index}_{id_quiz}_{current_question[-1]}_{annotation}"
        keyboard_markup.add(types.InlineKeyboardButton(text=f"Ответ {i+1}", callback_data=callback_data))
    keyboard_markup.add(types.InlineKeyboardButton("Закончить тест", callback_data="mode_back"))
    await bot.edit_message_reply_markup(chat_id, message.message_id, reply_markup=keyboard_markup)

async def check_answer(query: types.CallbackQuery):
    await query.message.delete()
    selected_answer, correct_answer, question_index,id_quiz, id_answer, annotation = [
    int(x) for x in query.data.split('_')[1:]][-6:]
    # если ответ верный, увеличиваем количество правильных ответов
    db.right_answer(id_quiz) if selected_answer == correct_answer else db.wrong_answer(id_answer,id_quiz)
    # получаем все вопросы теста из базы данных
    
    array = db.get_qustions(id_quiz)
    my_list = array[0].split(', ')
    answers = db.get_answer_exam(my_list) if annotation != 2 else db.get_answer_exam(my_list[:-1])
    # если есть еще вопросы, отправляем следующий вопрос
    if question_index < len(answers) - 1:     
        await send_question(query.message.chat.id, question_index + 1, answers,id_quiz,annotation)
    else:
        # иначе выводим результаты теста #PR ошибки кнопку
        result = db.get_quiz_result(id_quiz)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Назад", callback_data="mode_back"))

        await bot.send_message(query.message.chat.id, f"Результат:\nКол-во вопросов: {len(answers)}\nКол-во правильных ответов: {result}\nОшибки можно отработать в разделе <Ошибки>",reply_markup=markup)
        







async def show_category(chat_id: int, index = 0):
    markup = create_category(index)
    await bot.send_message(chat_id, "Выберите категорию", reply_markup=markup)


def create_category(index):
    markup = types.InlineKeyboardMarkup(row_width=1)
    category = [    "Безопасность движения и техника управления автомобилем",    "Буксировка механических транспортных средств",    "Движение в жилых зонах",    "Движение по автомагистралям",    "Движение через железнодорожные пути",    "Дорожная разметка",    "Дорожные знаки",    "Начало движения маневрирование",    "Неисправности и условия допуска транспортных средств к эксплуатации",    "Обгон опережение встречный разъезд",    "Общие обязанности водителей",    "Общие положения",    "Оказание доврачебной медицинской помощи",    "Остановка и стоянка",    "Ответственность водителя",    "Перевозка людей и грузов",    "Пешеходные переходы и места остановок маршрутных транспортных средств",    "Пользование внешними световыми приборами и звуковыми сигналами",    "Применение аварийной сигнализации и знака аварийной остановки",    "Применение специальных сигналов",    "Приоритет маршрутных транспортных средств",    "Проезд перекрестков",    "Расположение транспортных средств на проезжей части",    "Сигналы светофора и регулировщика",    "Скорость движения",    "Учебная езда и дополнительные требования к движению велосипедистов"]
    # Первая строка - месяц и год
    row = [types.InlineKeyboardButton("◀️", callback_data=f"cat-prev-{index}"),
           types.InlineKeyboardButton("Категории:", callback_data="ignore"),
           types.InlineKeyboardButton("▶️", callback_data=f"cat-next-{index}")]
    markup.row(*row)   
    # Остальные строки - дни месяца
    count = 6 if index == 20 else 5
    for i in range(index,index+count): 
            markup.add(types.InlineKeyboardButton(str(category[i]), callback_data = f"category_{i}"))          
    markup.add(types.InlineKeyboardButton("Выйти", callback_data="mode_back"))
    return markup


async def cat_prev_callback(query):
    index = query.data.split('-')[-1]
    index = int(index)
    index-=5 if index !=0 else 0
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  reply_markup=create_category(index))

async def cat_next_callback(query):
    index = query.data.split('-')[-1]
    index = int(index)
    index+=5 if index <20 else 0
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                        reply_markup=create_category(index))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_exam, lambda message: message.text == "✅ Пройти экзамен ПДД" )
    dp.register_callback_query_handler(mode_quiz, lambda query: query.data.startswith('mode_'))
    dp.register_callback_query_handler(bilet_mode, lambda query: query.data.startswith('bilet_'))
    dp.register_callback_query_handler(check_answer, lambda query: query.data.startswith('answer_'))
    dp.register_callback_query_handler(cat_next_callback, lambda query: query.data.startswith('cat-next-'))
    dp.register_callback_query_handler(cat_prev_callback, lambda query: query.data.startswith('cat-prev-'))
    dp.register_callback_query_handler(category_mode, lambda query: query.data.startswith('category_'))

