from utils import db_followers
from datetime import datetime
import random
from utils import log

logger = log.get_logger()


def inserir_pendentes_db(bot, contas_desejadas, qtd_seguidores_por_conta):
    todos_seguidores = []
    for conta in contas_desejadas:
        seguidores_conta = bot.get_user_followers(conta, qtd_seguidores_por_conta)
        todos_seguidores.extend(seguidores_conta)
    insert_novos = []
    for novo in todos_seguidores:
        username = bot.get_username_from_user_id(novo)
        if username is None:
            logger.error("Algo deu errado na funcao inserir_pendentes_db ao obter o nome de usuário. Melhor parar.")
            return False
        user = (novo, username, datetime.now(), 1)
        logger.info(f"Novo pendente a ser inserido no banco: {user}")
        insert_novos.append(user)
    db_followers.insert_many_users(insert_novos)
    return True


def buscar_usuarios_pendentes_para_seguir():
    sql = "SELECT USER_ID, USER_NAME FROM users WHERE STATUS = 1"
    ret = db_followers.executar_select(sql)
    return ret


def buscar_usuarios_pendentes_para_deixar_de_seguir():
    sql = '''
        SELECT USER_ID, USER_NAME
        FROM users WHERE STATUS = 2
        AND ULTIMA_ATUALIZACAO < DATE()
        ORDER BY ULTIMA_ATUALIZACAO
    '''
    ret = db_followers.executar_select(sql)
    return ret


def follow(bot, contas_desejadas):
    try:
        logger.warning("---> Iniciando ação FOLLOW")
        pendentes = buscar_usuarios_pendentes_para_seguir()
        logger.info(f"Tamanho total da lista de pendentes para seguir: {len(pendentes)}")
        if len(pendentes) > 0:
            seguidor_escolhido = random.choice(pendentes)
            logger.info(f"Seguindo seguidor: {seguidor_escolhido[1]}")
            sucesso = bot.follow(seguidor_escolhido[0])
            if not sucesso:
                logger.error("Algo deu errado. Parando o processo.")
                return False
            logger.info(f"Seguidor {seguidor_escolhido[1]} seguido com sucesso!")
            db_followers.update_user_status(seguidor_escolhido[0], 2)
            return True
        else:
            success = inserir_pendentes_db(bot, contas_desejadas, 50)
            if not success:
                return False
    except Exception as e:
        logger.error(f"Erro ao executar o processo: {e}")
        return False


def unfollow(bot):
    try:
        logger.warning("---> Iniciando ação UNFOLLOW")
        pendentes = buscar_usuarios_pendentes_para_deixar_de_seguir()
        logger.info(f"Tamanho total da lista de pendentes para deixar de seguir: {len(pendentes)}")
        if len(pendentes) > 0:
            seguidor_escolhido = random.choice(pendentes)
            logger.info(f"Deixando de seguir: {seguidor_escolhido[1]}")
            sucesso = bot.unfollow(seguidor_escolhido[0])
            if not sucesso:
                logger.error("Algo deu errado. Parando o processo.")
                return False
            logger.info(f"Seguidor {seguidor_escolhido[1]} deixado de ser seguido com sucesso!")
            db_followers.update_user_status(seguidor_escolhido[0], 3)
            return True
    except Exception as e:
        logger.error(f"Erro ao executar o processo: {e}")
        return False
