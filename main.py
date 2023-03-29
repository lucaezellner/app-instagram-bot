import os
import random
import time
from dotenv import load_dotenv
from instagrapi import Client
from utils import actions
from utils import log

load_dotenv()

log.add_logging_level("FOLLOW", 25)
log.add_logging_level("UNFOLLOW", 26)
logger = log.get_logger()

bot = Client()

logger.info("Iniciando login...")
bot.login(username=os.environ['usuario'], password=os.environ['senha'])
logger.info("Login realizado com sucesso!")

contas_desejadas = ["eusoupaulinholima", "rodrigocohenoficial", "rafaelhaguiwara", "ottogsparenberg"]

counter = 1
keep_following = True
keep_unfollowing = True
retentativas_follow = 1
retentativas_unfollow = 1
while True:
    # AÇÃO FOLLOW
    if keep_following:
        sucesso = actions.follow(bot, contas_desejadas)
        if sucesso:
            retentativas_follow = 1
            logger.follow(f"Ação FOLLOW finalizada com sucesso na {counter}ª iteração.")
        else:
            if retentativas_follow < 2:
                retentativas_follow += 1
                logger.error(f"Ação FOLLOW finalizada com erro na {counter}ª iteração. Irá tentar novamente...")
            else:
                keep_following = False
                logger.critical(f"Ação FOLLOW finalizada com erro na {counter}ª iteração.")
                logger.critical(f"Número de retentativas excedido para FOLLOW. Desligando FOLLOW.")
    time.sleep(random.randint(200, 300))
    # AÇÃO UNFOLLOW
    if keep_unfollowing:
        sucesso = actions.unfollow(bot)
        if sucesso:
            retentativas_unfollow = 1
            logger.unfollow(f"Ação UNFOLLOW finalizada com sucesso na {counter}ª iteração.")
        else:
            if retentativas_unfollow < 2:
                retentativas_unfollow += 1
                logger.error(f"Ação UNFOLLOW finalizada com erro na {counter}ª iteração. Irá tentar novamente...")
            else:
                keep_unfollowing = False
                logger.critical(f"Ação UNFOLLOW finalizada com erro na {counter}ª iteração.")
                logger.critical(f"Número de retentativas excedido para UNFOLLOW. Desligando UNFOLLOW.")
    time.sleep(random.randint(100, 200))
    # CASO CRITICO DE ERROS
    if not keep_following and not keep_unfollowing:
        logger.critical("Algo deu errado. Parando o robô.")
        break
    counter += 1
