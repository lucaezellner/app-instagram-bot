import os
import random
import time
from dotenv import load_dotenv
from instagrapi import Client
from utils import actions
from utils import log
import atexit

load_dotenv()

RETENTATIVAS = 3
DELAY_FOLLOW = random.randint(300, 400)
DELAY_UNFOLLOW = random.randint(200, 400)
USERNAME = os.environ['usuario']
PASSWORD = os.environ['senha']
# Necessário para cores de logs no terminal
os.system("")

log.add_logging_level("FOLLOW", 25)
log.add_logging_level("UNFOLLOW", 26)
logger = log.get_logger()

bot = Client()
bot.set_locale("pt_BR")
bot.set_country("BRA")
bot.set_country_code(55)
bot.set_timezone_offset(-3 * 60 * 60)


@atexit.register
def logout():
    logger.info("Finalizando programa. Logout iniciado!")
    bot.logout()
    logger.info("Logout concluído.")


def dormir(delay):
    m, s = divmod(delay, 60)
    logger.info(f"Irá dormir por {m:02d}:{s:02d}.")
    time.sleep(delay)


logger.info("Iniciando login...")
bot.login(username=USERNAME, password=PASSWORD)
bot.dump_settings('session.json')
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
        status_action = actions.follow(bot, contas_desejadas)
        if status_action["sucesso"]:
            retentativas_follow = 1
            logger.follow(f"Ação FOLLOW finalizada com sucesso na {counter}ª iteração.")
        else:
            if status_action["continuar"]:
                if retentativas_follow < RETENTATIVAS:
                    retentativas_follow += 1
                    logger.error(f"Ação FOLLOW finalizada com erro na {counter}ª iteração. Irá tentar novamente...")
                else:
                    keep_following = False
                    logger.critical(f"Ação FOLLOW finalizada com erro na {counter}ª iteração.")
                    logger.critical(f"Número de retentativas excedido para FOLLOW. Desligando FOLLOW.")
            else:
                keep_following = False
    dormir(DELAY_FOLLOW)

    # AÇÃO UNFOLLOW
    if keep_unfollowing:
        status_action = actions.unfollow(bot)
        if status_action["sucesso"]:
            retentativas_unfollow = 1
            logger.unfollow(f"Ação UNFOLLOW finalizada com sucesso na {counter}ª iteração.")
        else:
            if status_action["continuar"]:
                if retentativas_unfollow < RETENTATIVAS:
                    retentativas_unfollow += 1
                    logger.error(f"Ação UNFOLLOW finalizada com erro na {counter}ª iteração. Irá tentar novamente...")
                else:
                    keep_unfollowing = False
                    logger.critical(f"Ação UNFOLLOW finalizada com erro na {counter}ª iteração.")
                    logger.critical(f"Número de retentativas excedido para UNFOLLOW. Desligando UNFOLLOW.")
            else:
                keep_unfollowing = False
    dormir(DELAY_UNFOLLOW)

    # CASO CRITICO DE ERROS
    if not keep_following and not keep_unfollowing:
        logger.critical("Algo deu errado. Parando o robô.")
        break
    counter += 1
