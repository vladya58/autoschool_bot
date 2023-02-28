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
    
    