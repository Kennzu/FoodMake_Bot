import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime
import os

def run_migrate():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='root',
        )

        cur = db.cursor()
        
        with open('src/migrations/001_init_tables.sql', 'r', encoding="utf-8") as f:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                command = command.strip()
                if command:
                    cur.execute(command)
        db.commit()
        db.close()
        logging.info("Успешно выполнены миграции")
    except Error as er:
        print(f"Failed to connect: {er}")
        return None
    
def backup_database():
    """Создает полный дамп базы данных"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='root',
        )

        # conn = mysql.connector.connect(
        #     host='db_food',  # Имя контейнера
        #     user='admin_user',
        #     password='tristam100!!',
        #     database='food_list',
        #     port=3306)  # Стандартный порт MySQL

        cursor = conn.cursor()
        # Генерируем имя файла с текущей датой
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join('src/backups/', f"backup_{timestamp}.sql")
        
        # Получаем список всех таблиц
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        # Создаем файл дампа
        with open(backup_file, 'w', encoding='utf-8') as f:
            for table in tables:
                # Записываем структуру таблицы
                cursor.execute(f"SHOW CREATE TABLE {table}")
                create_table = cursor.fetchone()[1]
                f.write(f"\n\n-- Структура таблицы {table}\n")
                f.write(f"{create_table};\n")
                
                # Записываем данные таблицы
                f.write(f"\n-- Данные таблицы {table}\n")
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                if rows:
                    columns = [i[0] for i in cursor.description]
                    f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n")
                    
                    for i, row in enumerate(rows):
                        values = []
                        for value in row:
                            if value is None:
                                values.append("NULL")
                            elif isinstance(value, (int, float)):
                                values.append(str(value))
                            else:
                                # Исправленная строка с правильным экранированием кавычек
                                values.append(f"""{str(value).replace("'", "''")}""")
                        
                        row_str = f"({', '.join(values)})"
                        if i < len(rows) - 1:
                            row_str += ",\n"
                        else:
                            row_str += ";\n"
                        f.write(row_str)
        
        print(f"Резервная копия успешно создана: {backup_file}")
        return backup_file
        
    except Error as e:
        print(f"Ошибка при создании резервной копии: {e}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    
if __name__ == "__main__":
    run_migrate()

