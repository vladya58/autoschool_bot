from aiogram import executor
from handlers import menu, lk,rec_lesson, exam_pdd, other,payment,edit_lesson,command_menu
from create_bot import dp


menu.register_handlers(dp)
lk.register_handlers(dp)
rec_lesson.register_handlers(dp)
payment.register_handlers(dp)
edit_lesson.register_handlers(dp)
exam_pdd.register_handlers(dp)
command_menu.register_handlers(dp)


other.register_handlers(dp)




if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)





