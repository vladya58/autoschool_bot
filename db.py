import sqlite3


import psycopg2


class Database:
    def __init__(self,db):
        self.connection = psycopg2.connect(
    
            host="localhost",
            port = "5432",
            database="Autoshool58",
            user="postgres",
            password="Qwerty58"
        )

        self.cursor = self.connection.cursor()

    def check_rules_teacher(self,user_id):
        
        with self.connection:
            self.cursor.execute("SELECT id_teacher FROM teachers WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchone()
            return result[0]

    def get_full_teacher_data(self,user_id):
        with self.connection:
            self.cursor.execute(
                """
                SELECT t.id_teacher,t.user_id, t.phone_number, t.name, t.age, t.experiance, t.email,
                c.transmisson, c.brand, c.color, c.number
                FROM teachers AS t
                LEFT JOIN cars AS c
                ON t.id_teacher = c.id_teacher
                WHERE t.user_id = %s
                """, 
                (user_id,)
            )
            result = self.cursor.fetchone()
            return result

    def get_lessons_days(self,id_teacher,datetime,ids=False):
        with self.connection:
            coin = ">=" if ids == False else "<="
            self.cursor.execute(
            f"""
            SELECT DISTINCT ON (date) date
            FROM timetable_practic
            WHERE id_teacher = {id_teacher} AND date {coin} '{datetime}'
            ORDER BY date ASC
            """
        )
            result = self.cursor.fetchall()
            return result

    def get_lesson_on_day(self,id_teacher,datetime):
         with self.connection:
            self.cursor.execute(
            """
            SELECT id_practic,date,time,id_student
                FROM timetable_practic
                WHERE id_teacher = %s AND date = %s
                """, 
            (id_teacher, datetime)
        )
            result = self.cursor.fetchall()
            return result

    def check_rul_examen(self,user_id,name_exam):
        if name_exam == 0:
            with self.connection:
                self.cursor.execute(
                """
                SELECT 
                (SELECT count_lessons FROM students WHERE user_id = %s) >= 
                (SELECT practic_count 
                FROM students s
                INNER JOIN groups g ON s.id_group = g.id_group
                INNER JOIN program p ON g.id_program = p.id_program
                WHERE s.user_id = %s) as result""", 
                (user_id,user_id)
            )
                
                result = self.cursor.fetchone()
            

                return result

    
    def del_lesson_on_day(self,id_teacher,datetime):
         
        with self.connection:
           
           return self.cursor.execute("DELETE FROM timetable_practic WHERE date = %s AND id_teacher =%s",(datetime,id_teacher))

    def update_count_lesson(self,id):
        with self.connection:
           
           return self.cursor.execute("UPDATE students SET count_lessons = count_lessons + 1 WHERE id_student = %s",(id,))
        

    
    def get_info_lesson(self,id):
        with self.connection:
            lst = []
            self.cursor.execute(
            """
            SELECT tp.date, tp.time, s.name, s.phone_number, s.email, c.adres, c.room, s.id_student
            FROM timetable_practic tp
            JOIN students s ON tp.id_student = s.id_student
            JOIN class c ON tp.id_class = c.id_class
            WHERE tp.id_practic = %s
                """, 
            (id,)
        )
            
            result = self.cursor.fetchone()
            return result
        
                
    
    

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'students' ('user_id') VALUES (?)", (user_id,))
    
    def user_exists(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT * FROM students WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchall()
            return bool(len(result))
        
    def phone_exists(self,phone):
        with self.connection:
            self.cursor.execute("SELECT * FROM students WHERE phone_number = %s", (phone,))
            result = self.cursor.fetchall()
            # result = self.cursor.execute (f"SELECT * FROM students WHERE phone_number = '{phone}'").fetchall()
            return bool(len(result))

    def get_full_data(self,user_id,ids = False):
        if ids == False:
            with self.connection:
                self.cursor.execute("SELECT user_id,phone_number,name,pasport,medical,email,age,id_group,balance FROM students WHERE user_id = %s", (user_id,))
                result = self.cursor.fetchall()
                #result = self.cursor.execute (f"SELECT user_id,phone_number,name,pasport,medical,email,age,id_group FROM students WHERE user_id = '{user_id}'").fetchall()
                return result[0]
        elif ids == True:

            self.cursor.execute("SELECT user_id,phone_number,name,pasport,medical,email,age,id_group,balance FROM students WHERE id_student = %s", (user_id,))
            result = self.cursor.fetchall()
            #result = self.cursor.execute (f"SELECT user_id,phone_number,name,pasport,medical,email,age,id_group FROM students WHERE user_id = '{user_id}'").fetchall()
            return result[0]


    def get_balance(self,user_id):
        with self.connection:
            self.cursor.execute("SELECT balance FROM students WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchone()
            
            return result[0]


    def set_user_id(self,user_id, phone):
        with self.connection:
           
           return self.cursor.execute("UPDATE students SET user_id = %s WHERE phone_number = %s", (user_id, phone,)) #self.cursor.execute("UPDATE students SET user_id = ? WHERE phone_number = ?",(user_id, phone))
    
    def get_full(self,user_id): #Проверка заполнены ли все данные.
        with self.connection:
            self.cursor.execute("SELECT full_reg FROM students WHERE user_id = %s", (user_id,))
            #result = self.cursor.execute (f"SELECT full_reg FROM students WHERE user_id = '{user_id}'")
            result = self.cursor.fetchone() 
            return result[0]
    def get_email(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT email FROM students WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchone() 
            return result[0]


    def set_signup(self, user_id, signup):
        with self.connection:
           return self.cursor.execute("UPDATE 'students' SET 'signup' = ? WHERE 'user_id' = ?", (signup, user_id))
    
    def set_name(self,user_id, name):
        with self.connection:
           return self.cursor.execute("UPDATE students SET name = %s WHERE user_id = %s",(name, user_id))
    
    def set_pasport(self,user_id, pasport):
        with self.connection:
           return self.cursor.execute("UPDATE students SET pasport = %s WHERE user_id = %s",(pasport, user_id))

    def set_medical(self,user_id, medical):
        with self.connection:
           return self.cursor.execute("UPDATE students SET medical = %s WHERE user_id = %s",(medical, user_id))
    
    def set_email(self,user_id, email):
        with self.connection:
           return self.cursor.execute("UPDATE students SET email = %s WHERE user_id = %s",(email, user_id))
        
    def set_age(self,user_id, age):
        with self.connection:
           return self.cursor.execute("UPDATE students SET age = %s WHERE user_id = %s",(age, user_id))


    def get_data(self,user_id):
        with self.connection:
            self.cursor.execute("SELECT name,pasport,medical,email,age FROM students WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchall()
            return result[0]
    def get_data_of_payment(self,user_id):
        with self.connection:
            self.cursor.execute("SELECT phone_number,name,balance FROM students WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchall()
            return result[0]
        
    def set_full(self,user_id):
        with self.connection:
           return self.cursor.execute("UPDATE students SET full_reg = %s WHERE user_id = %s",(True, user_id))
        
    def check_table(self, user_id, month, day,year = "2023"):
    
        data_str = f"{year}-{month.rjust(2, '0')}-{day.rjust(2, '0')}"
        with self.connection:
            self.cursor.execute("SELECT tp.time FROM students s JOIN groups g ON s.id_group = g.id_group JOIN timetable_practic tp ON g.id_teacher = tp.id_teacher WHERE s.user_id = %s AND tp.date = %s", (user_id,data_str, ))
    
            result = self.cursor.fetchall()
            return result
    
    def rec_lesson(self,user_id, date, time):
        with self.connection:

            self.cursor.execute("INSERT INTO timetable_practic (date, time, id_teacher, id_lesson, id_student) SELECT %s, %s, groups.id_teacher, %s, students.id_student FROM students JOIN groups ON students.id_group = groups.id_group WHERE students.user_id = %s", (date,time, 1, user_id, ))
    
    def rec_exam(self,user_id,date, id_lesson): 
        with self.connection:
            self.cursor.execute("INSERT INTO students_of_exam (id_exam, id_student) SELECT (SELECT id_exam FROM gibdd_exam WHERE date_exam = %s AND id_lesson = %s), id_student FROM students WHERE user_id = %s", (date, id_lesson,user_id,))
            

    def get_lessons_pr(self,user_id,date,id_lesson = 1):
        with self.connection:
            self.cursor.execute("SELECT tp.date, tp.time, tp.id_teacher,tp.id_class, tp.id_lesson, tp.id_practic tp FROM timetable_practic tp JOIN students s ON tp.id_student = s.id_student WHERE s.user_id = %s AND tp.id_lesson = %s AND tp.date >= %s", (user_id, id_lesson, date))
            result = self.cursor.fetchall()
            return result
        
    def get_lessons_tr(self,user_id,id_lesson = 2):
        with self.connection:
            self.cursor.execute("""
                SELECT t.day_week, t.time, t.id_teacher, t.id_class, t.id_lesson, t.id_teory
                FROM timetable_teory t
                JOIN students s ON t.id_group = s.id_group
                WHERE s.user_id = %s AND t.id_lesson = %s
            """, (user_id, id_lesson))
            result = self.cursor.fetchone()

        

            return result
            
    def get_ihfoles(self, id_teacher, id_class):
         with self.connection:
            self.cursor.execute("SELECT name, phone_number, email FROM teachers WHERE id_teacher = %s", (id_teacher,))
            info_teacher = self.cursor.fetchone()
            self.cursor.execute("SELECT adres, room FROM class WHERE id_class = %s", (id_class,))
            info_class = self.cursor.fetchone()
            return info_teacher, info_class



    def get_exams_student(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT gibdd_exam.id_lesson, gibdd_exam.date_exam, gibdd_exam.name_inspector, students_of_exam.id_rec_exam FROM gibdd_exam JOIN students_of_exam ON gibdd_exam.id_exam = students_of_exam.id_exam JOIN students ON students_of_exam.id_student = students.id_student WHERE gibdd_exam.date_exam >= NOW() AND students.user_id = %s", (user_id,))
            arr = self.cursor.fetchall()
            return arr

    

    def del_exam(self,id):
        with self.connection:
           return self.cursor.execute("DELETE FROM students_of_exam WHERE id_rec_exam = %s",(id,))



    def del_lesson(self, id,ids=False):
        if ids == False:
            with self.connection:
                return self.cursor.execute("DELETE FROM timetable_practic WHERE id_practic = %s",(id,))

        elif ids == True:
            with self.connection:
                self.cursor.execute("SELECT id_student FROM timetable_practic WHERE id_practic = %s", (id,))
                id_student = self.cursor.fetchone()[0]
                self.cursor.execute("DELETE FROM timetable_practic WHERE id_practic = %s", (id,))
                return id_student
            


    def show_date_exam(self,id_lesson,date):
        with self.connection:
            self.cursor.execute("SELECT id_exam, date_exam ,count_students FROM gibdd_exam WHERE id_lesson = %s AND date_exam > %s ", (id_lesson,date,))
            result = self.cursor.fetchall()
            return result
        
    def show_count_slots(self,id_exam):
         with self.connection:
            self.cursor.execute("SELECT id_student  FROM students_of_exam WHERE id_exam = %s", (id_exam,))
            
            result = self.cursor.fetchall()
            return result
         

    def get_payment(self,user_id):
        with self.connection:
            self.cursor.execute("SELECT p.date, p.time, p.amount, p.source FROM payment p JOIN students s ON s.id_student = p.id_student WHERE s.user_id = %s", (user_id,))
            result = self.cursor.fetchall()
            return result



    def set_payment(self,user_id, date,time,amount,currency,charge_id,source):
        with self.connection:
            self.cursor.execute("INSERT INTO payment (id_student, date, time, amount, currency, provider_payment_charge_id, source) SELECT s.id_student, %s, %s, %s, %s, %s, %s FROM students s WHERE s.user_id = %s RETURNING id", (date,time,amount,currency,charge_id,source,user_id))
            result = self.cursor.fetchone()
            return result[0]
    def update_balance(self,user_id,amount,ids = False):
        if ids == False:
            with self.connection:
                self.cursor.execute("UPDATE students SET balance = balance + %s WHERE id_student = (SELECT id_student FROM students WHERE user_id = %s);", (amount, user_id))
        elif ids == True:
            with self.connection:
                self.cursor.execute("UPDATE students SET balance = balance + %s WHERE id_student = %s;", (amount,user_id))
       

    def get_answer_exam(self,questions):
        if isinstance(questions, list):
            ids = tuple(questions)
        else:
            ids = questions
        with self.connection:
            self.cursor.execute("SELECT path_to_image, count_answ, right_answ, text, anotation, id_exam_quest FROM exam_pdd WHERE id_exam_quest IN %s", (ids,))
            result = self.cursor.fetchall()
            return result
    def get_qustions(self,id_quiz):
        with self.connection:
            self.cursor.execute("SELECT array_q FROM result_quiz WHERE id = %s", (id_quiz,))
            result = self.cursor.fetchone()
            return result
        

    def get_qustions_error(self,user_id):
        with self.connection:
            self.cursor.execute("SELECT errors FROM result_quiz WHERE id_student = (SELECT id_student FROM students WHERE user_id = %s) ORDER BY id DESC LIMIT 1", (user_id,))
            result = self.cursor.fetchone()
            return result[0]


    def get_answers_hard(self,):
        with self.connection:
            self.cursor.execute("SELECT path_to_image, count_answ, right_answ, text, anotation, id_exam_quest FROM exam_pdd WHERE hard = %s", (True,))
            result = self.cursor.fetchall()
            return result
        

    def get_answers_category(self, category):
        with self.connection:
            self.cursor.execute("SELECT path_to_image, count_answ, right_answ, text, anotation, id_exam_quest FROM exam_pdd WHERE notion LIKE %s", ("%" + category + "%",))
            result = self.cursor.fetchall()
            return result

    def get_answers_bilet(self, bilet):
        with self.connection:
            self.cursor.execute("SELECT path_to_image, count_answ, right_answ, text, anotation, id_exam_quest FROM exam_pdd WHERE bilet = %s", (bilet,))
            result = self.cursor.fetchall()
            return result

    def start_quiz(self,user_id,time,mode):
        with self.connection:
            self.cursor.execute("INSERT INTO result_quiz(id_student, time_start, mode, result) VALUES ((SELECT id_student FROM students WHERE user_id = %s), %s, %s, %s) RETURNING id",
    (user_id, time, mode, 0))
            result = self.cursor.fetchone()
            return result[0]
    def set_questions_quiz(self,array,id_quiz):
        with self.connection:

            self.cursor.execute("UPDATE result_quiz SET array_q = %s WHERE id = %s", (array, id_quiz))
            

    def get_quiz_result(self,id_quiz):
        with self.connection:
            self.cursor.execute("SELECT result FROM result_quiz WHERE id = %s", (id_quiz,))
            result = self.cursor.fetchone()
            return result[0]

        
    def right_answer(self,id_quiz):
        with self.connection:
            self.cursor.execute("UPDATE result_quiz SET result = result + 1 WHERE id = %s",(id_quiz,))
    def wrong_answer(self,id_answer, id_quiz):
        with self.connection:
            self.cursor.execute("UPDATE result_quiz SET errors = CONCAT(errors, '%s, ') WHERE id = %s",(id_answer,id_quiz,))
    
