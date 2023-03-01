import sqlite3

class Database:
    def __init__(self,db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
    
    def user_exists(self,user_id):
        with self.connection:
            result = self.cursor.execute (f"SELECT * FROM users WHERE user_id = '{user_id}'").fetchall()
            return bool(len(result))
        
    def phone_exists(self,phone):
        with self.connection:
            result = self.cursor.execute (f"SELECT * FROM users WHERE phone = '{phone}'").fetchall()
            return bool(len(result))

    def get_full_data(self,user_id):
        with self.connection:
            result = self.cursor.execute (f"SELECT user_id,phone,name,pasport,medical,email,age,class FROM users WHERE user_id = '{user_id}'").fetchall()
            return result[0]

    
    def set_user_id(self,user_id, phone):
        with self.connection:
           return self.cursor.execute("UPDATE users SET user_id = ? WHERE phone = ?",(user_id, phone))
    
    def get_full(self,user_id): #Проверка заполнены ли все данные.
        with self.connection:
            result = self.cursor.execute (f"SELECT full FROM users WHERE user_id = '{user_id}'").fetchone() 
            return result[0]


    def set_signup(self, user_id, signup):
        with self.connection:
           return self.cursor.execute("UPDATE 'users' SET 'signup' = ? WHERE 'user_id' = ?", (signup, user_id))
    
    def set_name(self,user_id, name):
        with self.connection:
           return self.cursor.execute("UPDATE users SET name = ? WHERE user_id = ?",(name, user_id))
    
    def set_pasport(self,user_id, pasport):
        with self.connection:
           return self.cursor.execute("UPDATE users SET pasport = ? WHERE user_id = ?",(pasport, user_id))

    def set_medical(self,user_id, medical):
        with self.connection:
           return self.cursor.execute("UPDATE users SET medical = ? WHERE user_id = ?",(medical, user_id))
    
    def set_email(self,user_id, email):
        with self.connection:
           return self.cursor.execute("UPDATE users SET email = ? WHERE user_id = ?",(email, user_id))
        
    def set_age(self,user_id, age):
        with self.connection:
           return self.cursor.execute("UPDATE users SET age = ? WHERE user_id = ?",(age, user_id))


    def get_data(self,user_id):
        with self.connection:
            result = self.cursor.execute (f"SELECT name,pasport,medical,email,age FROM users WHERE user_id = '{user_id}'").fetchall()
            return result[0]
        
    def set_full(self,user_id, full):
        with self.connection:
           return self.cursor.execute("UPDATE users SET full = ? WHERE user_id = ?",(full, user_id))
        
    


    