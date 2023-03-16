import sqlite3


import psycopg2

# # установка параметров подключения к базе данных
# conn = psycopg2.connect(
    
#     host="localhost",
#     port = "5432",
#     database="Autoshool58",
#     user="postgres",
#     password="Qwerty58"
# )

# # выполнение запроса на выборку данных
# cur = conn.cursor()
# cur.execute("SELECT * FROM Students")

# # получение результатов и вывод их на экран
# rows = cur.fetchall()
# for row in rows:
#     print(row)

# # закрытие соединения с базой данных
# cur.close()
# conn.close()

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
            # result = self.cursor.execute (f"SELECT name,pasport,medical,email,age FROM students WHERE user_id = '{user_id}'").fetchall()
            result = self.cursor.fetchall()
            return result[0]
        
    def set_full(self,user_id):
        with self.connection:
           return self.cursor.execute("UPDATE students SET full_reg = %s WHERE user_id = %s",(True, user_id))
        
    


    