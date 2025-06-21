import src.services.food_list_db as fld
import logging

def select_user(user_id):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()

        query = """SELECT * FROM users WHERE telegram_id = %s"""
        cur.execute(query, (user_id,))
        res_for_user_couples = cur.fetchall()
        logging.info(f"Информация по юзеру с пары: {res_for_user_couples}")
        return res_for_user_couples
    except Exception as e:
        logging.error(f"Не удалось достать данные по запросу: {e}")
        return None
    finally:
        if db:
            db.close()

def check_user(user_now):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()

        query = """SELECT telegram_id FROM users WHERE telegram_id = %s"""
        cur.execute(query, (user_now,))
        res_users = cur.fetchall()
        logging.info(f"Найден юзер по id: {res_users}")
        return bool(res_users)
        
    except Exception as e:
        logging.error(f"Не удалось получить данные с таблицы юзеров: {e}")
        return False
    finally:
        if db:
            db.close()


def create_user(telegram_id, username, first_name):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()

        query = """INSERT INTO users (telegram_id, username, first_name) VALUES (%s, %s, %s)"""
        cur.execute(query, (telegram_id, username, first_name))
        db.commit()

        cur.execute("""SELECT * FROM users""")
        res = cur.fetchall()
        print("pizdec", res)
    except Exception as e:
        logging.error("не удалось добавить юзера в базу: %s", str(e))
    finally:
        db.close()


def check_login(entered_login):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()

        query = """SELECT * FROM users WHERE username = %s"""
        cur.execute(query, (entered_login,))
        res_username = cur.fetchall()
        return bool(res_username)
    except Exception as e:
        logging.error("Не удалось получить данные из таблицы юзеров: %s", str(e))
    finally:
        db.close()
