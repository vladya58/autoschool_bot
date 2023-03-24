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

    def get_full_data(self,user_id):
        with self.connection:
            self.cursor.execute("SELECT user_id,phone_number,name,pasport,medical,email,age,id_group FROM students WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchall()
            #result = self.cursor.execute (f"SELECT user_id,phone_number,name,pasport,medical,email,age,id_group FROM students WHERE user_id = '{user_id}'").fetchall()
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
    
    def set_payment(self,user_id, date,amount,charge_id,currency,source):
        with self.connection:
            self.cursor.execute("INSERT INTO payment (id_student, date, amount, provider_payment_charge_id, currency, source) SELECT s.id_students, %s, %s, %s, %s, %s FROM students s WHERE s.user_id = %s;", (date,amount,charge_id,currency,source,user_id))
            
   
            
            


    