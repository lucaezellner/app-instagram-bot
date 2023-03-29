from utils import db_followers
from datetime import datetime
import random
from utils import log
from instagrapi.exceptions import LoginRequired

log.add_logging_level("FOLLOW", 25)
log.add_logging_level("UNFOLLOW", 26)
logger = log.get_logger()


def inserir_pendentes_db(bot, contas_desejadas, qtd_seguidores_por_conta):
    try:
        for conta in contas_desejadas:
            seguidores_conta = bot.user_followers(user_id=bot.user_id_from_username(conta), amount=qtd_seguidores_por_conta)
            insert_novos = []
            for novo_usuario in seguidores_conta:
                username = seguidores_conta[novo_usuario].username
                user = (novo_usuario, username, datetime.now(), 1)
                logger.info(f"Novo pendente a ser inserido no banco: {user}")
                insert_novos.append(user)
            db_followers.insert_many_users(insert_novos)
            logger.follow(f"Seguidores da conta '{conta}' inseridos no banco de dados com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao inserir usuários pendentes para seguir: {e}")
        return False


def buscar_usuarios_pendentes_para_seguir():
    sql = "SELECT USER_ID, USER_NAME FROM users WHERE STATUS = 1"
    ret = db_followers.executar_select(sql)
    return ret


def buscar_usuarios_pendentes_para_deixar_de_seguir():
    sql = '''
        SELECT USER_ID, USER_NAME, ULTIMA_ATUALIZACAO
        FROM users WHERE STATUS = 2
        AND ULTIMA_ATUALIZACAO < DATE('now', 'localtime')
        ORDER BY ULTIMA_ATUALIZACAO
    '''
    ret = db_followers.executar_select(sql)
    return ret


def follow(bot, contas_desejadas):
    seguidor_escolhido = (None, None)
    try:
        logger.info("Iniciando ação FOLLOW")
        pendentes = buscar_usuarios_pendentes_para_seguir()
        logger.info(f"Tamanho total da lista de pendentes para seguir: {len(pendentes)}")
        if len(pendentes) > 0:
            seguidor_escolhido = random.choice(pendentes)
            logger.info(f"Seguindo seguidor: {seguidor_escolhido[1]}")
            bot.user_follow(seguidor_escolhido[0])
            logger.follow(f"Seguidor {seguidor_escolhido[1]} seguido com sucesso!")
            db_followers.update_user_status(seguidor_escolhido[0], 2)
            return True
        else:
            logger.info(f"A lista de seguidores pendentes está vazia... Buscando novos nas contas {str(contas_desejadas)}")
            success = inserir_pendentes_db(bot, contas_desejadas, 50)
            if not success:
                return {"sucesso": False, "msg": "erro"}
            return True
    except LoginRequired as e:
        logger.warning(f"Erro na ação FOLLOW. {e}. Realizando novo login...")
        bot.relogin()
        logger.info("Relogin realizado com sucesso!")
        return False
    except Exception as e:
        db_followers.update_user_status(seguidor_escolhido[0], 4)
        logger.error(f"Erro no FOLLOW de {seguidor_escolhido[1]}. Status do seguidor alterado para ERROR.")
        logger.error(f"Erro ao executar o processo: {e}")
        return False


def unfollow(bot):
    seguidor_escolhido = (None, None)
    try:
        logger.info("Iniciando ação UNFOLLOW")
        pendentes = buscar_usuarios_pendentes_para_deixar_de_seguir()
        logger.info(f"Tamanho total da lista de pendentes para deixar de seguir: {len(pendentes)}")
        if len(pendentes) > 0:
            seguidor_escolhido = pendentes[0]
            logger.info(f"Deixando de seguir: {seguidor_escolhido[1]}. Havia sido seguido em {seguidor_escolhido[2]}")
            sucesso = bot.user_unfollow(seguidor_escolhido[0])
            if not sucesso:
                db_followers.update_user_status(seguidor_escolhido[0], 4)
                logger.error(f"Erro no UNFOLLOW de {seguidor_escolhido[1]}. Status do seguidor alterado para ERROR.")
                return False
            logger.unfollow(f"Seguidor {seguidor_escolhido[1]} deixado de ser seguido com sucesso!")
            db_followers.update_user_status(seguidor_escolhido[0], 3)
            return True
        else:
            logger.info("Não resta ninguém para deixar de seguir.")
            return True
    except LoginRequired as e:
        logger.warning(f"Erro na ação UNFOLLOW. {e}. Realizando novo login...")
        bot.relogin()
        logger.info("Relogin realizado com sucesso!")
        return False
    except Exception as e:
        db_followers.update_user_status(seguidor_escolhido[0], 4)
        logger.error(f"Erro no FOLLOW de {seguidor_escolhido[1]}. Status do seguidor alterado para ERROR.")
        logger.error(f"Erro ao executar o processo: {e}")
        return False
