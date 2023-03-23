import sqlite3
from datetime import datetime
from utils import log

if __name__ == "__main__":
    logger = log.get_logger()


def executar_query(query):
    try:
        con = sqlite3.connect("followers.db")
        cursor = con.cursor()
        cursor.execute(query)
        cursor.close()
        con.close()
    except Exception as e:
        logger.error(f"Erro ao executar a query {query}: {e}.")
        cursor.close()
        con.close()


def insert_user(user_id, user_name, ultima_atualizacao, status):
    try:
        con = sqlite3.connect("followers.db")
        cursor = con.cursor()

        sql = f"INSERT INTO users" \
              f"(USER_ID,USER_NAME,ULTIMA_ATUALIZACAO,STATUS)" \
              f"VALUES({user_id}, '{user_name}', '{ultima_atualizacao}', '{status}');"

        cursor.execute(sql)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        logger.error(f"Erro ao executar a query {sql}: {e}.")
        cursor.close()
        con.close()


def insert_many_users(list_users):
    try:
        con = sqlite3.connect("followers.db")
        cursor = con.cursor()

        sql = f"INSERT OR IGNORE INTO users" \
              f"(USER_ID,USER_NAME,ULTIMA_ATUALIZACAO,STATUS)" \
              f"VALUES(?, ?, ?, ?);"

        cursor.executemany(sql, list_users)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        logger.error(f"Erro ao executar a query {sql}: {e}.")
        cursor.close()
        con.close()


def update_user_status(user, novo_status):
    try:
        con = sqlite3.connect("followers.db")
        cursor = con.cursor()

        sql = f'''
            UPDATE users
            SET STATUS = ?,
            ULTIMA_ATUALIZACAO = ?
            WHERE USER_ID = ?
        '''

        cursor.execute(sql, (novo_status, datetime.now(), user))
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        logger.error(f"Erro ao executar a query {sql}: {e}.")
        cursor.close()
        con.close()


def insert_many_status(list_status):
    try:
        con = sqlite3.connect("followers.db")
        cursor = con.cursor()

        sql = f"INSERT INTO user_status" \
              f"(STATUS, DS_STATUS)" \
              f"VALUES(?,?);"

        cursor.executemany(sql, list_status)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        logger.error(f"Erro ao executar a query {sql}: {e}.")
        cursor.close()
        con.close()


def executar_select(sql):
    try:
        con = sqlite3.connect("followers.db")
        cursor = con.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        return ret
    except Exception as e:
        logger.error(f"Erro ao executar a query {sql}: {e}.")
        cursor.close()
        con.close()
