import mysql.connector
from mysql.connector import Error

class DBManager:
    def __init__(self):
        self.db = None


    def connect_db(self):
        try:
            self.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='root',
            )

            return self.db
        except Error as er:
            print(f"Failed to connect: {er}")
            return None
        
    def close(self):
        if self.db and self.db.is_connected():
            self.db.close()

    def add_breakfast(self, data, get_uuid):
        cur = self.db.cursor()
        query = '''INSERT INTO food_breakfast (couple_uuid, name, description, calories, image) VALUES (%s, %s, %s, %s, %s)'''
        cur.execute(query, (get_uuid, data['name'], data['description'], data['calories'], data['photo']))
        self.db.commit()

    def add_lanch(self, data, get_uuid):
        cur = self.db.cursor()
        query = '''INSERT INTO food_lanch(couple_uuid, name, description, calories, image) VALUES (%s, %s, %s, %s, %s)'''
        cur.execute(query, (get_uuid, data['name'], data['description'], data['calories'], data['photo']))
        self.db.commit()

    def add_dinner(self, data, get_uuid):
        cur = self.db.cursor()
        query = '''INSERT INTO food_dinner (couple_uuid, name, description, calories, image) VALUES (%s, %s, %s, %s, %s)'''
        cur.execute(query, (get_uuid, data['name'], data['description'], data['calories'], data['photo']))
        self.db.commit()

    def select_breakfast(self, get_uuid):
        try:
            cur = self.db.cursor(dictionary=True)
            query = '''SELECT * FROM food_breakfast WHERE couple_uuid == %s'''
            cur.execute(query, (get_uuid,))
            res = cur.fetchall()
            return res
        except Error as e:
            print("Ошибка получения обедов")
            return None

    def select_lanch(self, get_uuid):
        try:
            cur = self.db.cursor(dictionary=True)
            query = '''SELECT * FROM food_lanch WHERE couple_uuid == %s'''
            cur.execute(query, (get_uuid,))
            res_lanch = cur.fetchall()
            return res_lanch
        except Error as e:
            print("Ошибка получения обедов")
            return None

    def select_dinner(self, get_uuid):
        try:
            cur = self.db.cursor(dictionary=True)
            query = '''SELECT * FROM food_dinner WHERE couple_uuid == %s'''
            cur.execute(query, (get_uuid,))
            res_dinner = cur.fetchall()
            return res_dinner
        except Error as e:
            print("Ошибка получения ужинов")
            return None
        
    def one_dish_table(self, type_id, table):
        try:
            cur = self.db.cursor(dictionary=True)
            query = f'''SELECT * FROM {table} WHERE id = {int(type_id)}'''
            cur.execute(query)
            res_dish = cur.fetchall()
            return res_dish
        except Error as e:
            print("Ошибка получения блюда", e)
            return None

    def create_table(self):
        if not self.db:
            print("No database connection")
            return False
        cur = None
        try:
            cur = self.db.cursor()

            tables = [
                '''
                CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                username VARCHAR(255),
                first_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS couples_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                couple_uuid CHAR(36) UNIQUE,
                partner1_id BIGINT,
                partner2_id BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (partner1_id) REFERENCES users(telegram_id),
                FOREIGN KEY (partner2_id) REFERENCES users(telegram_id),
                UNIQUE (partner1_id, partner2_id)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS couple_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id BIGINT,
                receiver_id BIGINT,
                status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(telegram_id),
                FOREIGN KEY (receiver_id) REFERENCES users(telegram_id)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS subscriptions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                couple_uuid CHAR(36) UNIQUE,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (couple_id) REFERENCES couples_user(id)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS food_breakfast (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    couple_uuid CHAR(36) UNIQUE,
                    name VARCHAR(50) NOT NULL,
                    description TEXT,
                    calories INT,
                    image TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (couple_id) REFERENCES couples_user(id)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS food_lanch (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    couple_uuid CHAR(36) UNIQUE,
                    name VARCHAR(50) NOT NULL,
                    description TEXT,
                    calories INT,
                    image TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (couple_id) REFERENCES couples_user(id)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS food_dinner (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    couple_uuid CHAR(36) UNIQUE,
                    name VARCHAR(50) NOT NULL,
                    description TEXT,
                    calories INT,
                    image TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (couple_id) REFERENCES couples_user(id)
                )
                '''
            ]

            for table_query in tables:
                cur.execute(table_query)
            
            self.db.commit()
            print("Tables created successfully")
        except Error as er:
            print(f"Error creating tables: {er}")
            self.db.rollback()
        finally:
            if cur:
                cur.close()

db_manager = DBManager()