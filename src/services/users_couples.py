import src.services.food_list_db as fld
import logging

def check_couples(user_id):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()
        query = """SELECT * FROM couples_user WHERE partner1_id = %s OR partner2_id = %s"""
        cur.execute(query, (user_id, user_id))
        res_couple = cur.fetchall()
        logging.info("При проверке пары найдено: ", res_couple)
        return bool(res_couple)

    except Exception as e:
        logging.error("Ошибка проверки пары", e)
    finally:
        db.close()

def add_couple(partner1, partner2):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()
        query = """INSERT INTO couples_user (partner1_id, partner2_id) VALUES(%s, %s)"""
        cur.execute(query, (partner1, partner2,))
        db.commit()
        logging.info(f"Удалось создать пару между {partner1} и {partner2}")
    except Exception as e:
        logging.error("Ошибка при создании пары", e)
    finally:
        db.close()

def pending_status_couple(sender_id, receiver_id):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()
        query = """INSERT INTO couple_requests (sender_id, receiver_id) VALUES %s, %s"""
        cur.execute(query, (sender_id, receiver_id,))
        db.commit()
        logging.info(f"Запрос на пару создан: {sender_id} -> {receiver_id}")
    except Exception as e:
        logging.error(f"Не удалось создать запрос на создание пары с дефолт статусом {e}")
    finally:
        db.close()

def accepted_status_couple(receiver_id, gen_uuid):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()

        query = """SELECT sender_id FROM couple_requests WHERE reveiver_id == %s AND status == 'pending' ORDER BY created_at DESC LIMIT 1 """
        cur.execute(query, (receiver_id,))
        result = cur.fetchone()

        logging.info(f"Найден/не найден сендер в паре {result}")

        if not result:
            return None
        
        sender_id = result[0]

        update_query = """UPDATE couple_requests SET status = 'accepted' WHERE sender_id == %s and receiver_id == %s AND status == 'pending' """
        cur.execute(update_query, (sender_id, receiver_id,))

        insert_query = """INSERT INTO couples_user (couple_uuid, partner1_id, partner2_id) VALUES (%s, %s, %s)"""
        cur.execute(insert_query, (gen_uuid, sender_id, receiver_id))

        db.commit()
        logging.info(f"Пара была добавлена в базу {sender_id} + {receiver_id}")
        return sender_id
    except Exception as e:
        logging.error(f"Произошла ошибка при добавлении пары {e}")
    finally:
        db.close()

def get_uuid(user_id):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()

        query = """SELECT couple_uuid FROM couples_user WHERE partner1_id == %s or partner2_id == %s"""
        cur.execute(query, (user_id, user_id,))
        result_uuid = cur.fetchone()
        if result_uuid:
            uuid = result_uuid[0]
            return uuid
        else:
            return bool(result_uuid)
    except Exception as e:
        logging.error(f"При извлечении uuid произошла ошибка {e}")
    finally:
        db.close()

def get_couple(user_id):
    try:
        db = fld.db_manager.connect_db()
        cur = db.cursor()

        query = """SELECT * FROM couples_user WHERE partner1_id == %s or partner2_id == %s"""
        cur.execute(query, (user_id, user_id,))
        result_uuid = cur.fetchone()
        return result_uuid
    except Exception as e:
        logging.error(f"При попытке получить пару произошла ошибка {e}")
    finally:
        db.close()