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


async def menu_exam(message: types.Message):
    
    await bot.delete_message(message.chat.id, message.message_id)
    
    keyboard_rec = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Билеты", callback_data="mode_bilets")#types.InlineKeyboardButton(text="Авторизоваться", callback_data="log in")
    b2 = types.InlineKeyboardButton(text="Категории", callback_data="mode_category")
    b3 = types.InlineKeyboardButton(text="Самые сложные", callback_data="mode_hard")
    b4= types.InlineKeyboardButton(text="Экзамен", callback_data="mode_exam")
    b5= types.InlineKeyboardButton(text="Ошибки", callback_data="mode_errors")

    b6 = types.InlineKeyboardButton(text="Меню", callback_data="menu")
    

    keyboard_rec.add(b1,b2,b3,b4,b5,b6) 

    #PR сюда нужно ценую занятия.
    await message.answer('Вы перешли в меню тестирования! Выберите режим теста.', reply_markup=keyboard_rec)#reply_markup=types.ReplyKeyboardRemove()

async def mode_quiz(query: types.CallbackQuery):
    
    
    if "exam" in query.data:
        pass
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
        pass
    if "category" in query.data:
        pass
    if "errors" in query.data:
        pass


    if "back" in query.data:
        await menu_exam(query.message)
    
    




async def bilet_mode(query: types.CallbackQuery):
    await query.message.delete()
    # получаем все вопросы теста из базы данных
    answers = db.get_answers_bilet(query.data.split('_')[-1])
    id_quiz = db.start_quiz(query.from_user.id,datetime.datetime.now().time(),f"Билет {query.data.split('_')[-1]}")
    # начальный индекс вопроса
    question_index = 0
    correct_answers_count = 0
    # отправляем первый вопрос
    await send_question(query.message.chat.id, question_index,answers, answers[question_index][-1], id_quiz,query.data.split('_')[-1])

async def send_question(chat_id, question_index, answers,id_answer, id_quiz, bilet_number):
    # получаем информацию о текущем вопросе из списка ответов
    current_question = answers[question_index]
    # формируем сообщение с текстом вопроса и вариантами ответов
    
    quest, *text_answ = map(str.strip, current_question[3].split('\n'))
    text_answ = '\n'.join(text_answ).strip()
    

    hidden_text = hspoiler(f"{current_question[4]}")
    question_message = f"<b>{quest}</b>\n{text_answ}\n\nПодсказка:\n{hidden_text}"
    # если есть картинка, добавляем ее к сообщению
    if current_question[0] != "None":
        file_path = r"C:\pybot\images\A_B\eca08a0e2b5ffcd12bdd8ffee34afcc3.jpg"
        with open("C:/pybot/images/A_B/eca08a0e2b5ffcd12bdd8ffee34afcc3.jpg", 'rb') as photo:
            question_photo = types.InputMediaPhoto(photo)
            message = await bot.send_photo(chat_id, "https://blog.ukrnames.com/wp-content/uploads/2017/07/domain-name-360x240.jpg", caption=question_message,parse_mode='HTML')
    else:
        message = await bot.send_message(chat_id, question_message,parse_mode='HTML')
    # сохраняем правильный ответ
    correct_answer = current_question[2]
    keyboard_markup = types.InlineKeyboardMarkup()
    for i in range(current_question[1]):
        callback_data = f"answer_{i + 1}_{correct_answer}_{question_index}_{id_quiz}_{current_question[-1]}_{bilet_number}"
        keyboard_markup.add(types.InlineKeyboardButton(text=f"Ответ {i+1}", callback_data=callback_data))
    keyboard_markup.add(types.InlineKeyboardButton("Закончить тест", callback_data="mode_back"))
    await bot.edit_message_reply_markup(chat_id, message.message_id, reply_markup=keyboard_markup)

async def check_answer(query: types.CallbackQuery):
    await query.message.delete()
    selected_answer, correct_answer, question_index, id_answer, id_quiz, bilet_number = [
    int(x) for x in query.data.split('_')[1:]][-6:]
    # если ответ верный, увеличиваем количество правильных ответов
    db.right_answer(id_quiz) if selected_answer == correct_answer else db.wrong_answer(id_answer,id_quiz)
    # получаем все вопросы теста из базы данных
    answers = db.get_answers_bilet(bilet_number)
    
    # если есть еще вопросы, отправляем следующий вопрос
    if question_index < len(answers) - 1:     
        await send_question(query.message.chat.id, question_index + 1, answers,id_answer,id_quiz,bilet_number)
    else:
        # иначе выводим результаты теста
        result = db.get_quiz_result(id_quiz)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Назад", callback_data="mode_back"))

        await bot.send_message(query.message.chat.id, f"Результат {result} правильных ответа",reply_markup=markup)
        





def register_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_exam, lambda message: message.text == "✅ Пройти экзамен ПДД" )
    dp.register_callback_query_handler(mode_quiz, lambda query: query.data.startswith('mode_'))
    dp.register_callback_query_handler(bilet_mode, lambda query: query.data.startswith('bilet_'))
    dp.register_callback_query_handler(check_answer, lambda query: query.data.startswith('answer_'))

