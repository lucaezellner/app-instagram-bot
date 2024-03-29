import os
import random
from pathlib import Path
from dotenv import load_dotenv
from instagrapi import Client
from utils import actions
from utils import log
from utils.actions import verificar_login, dormir

load_dotenv()

RETENTATIVAS = 3
USERNAME = os.environ['usuario']
PASSWORD = os.environ['senha']
PATH_SESSION = Path(Path(__file__).parent, "session.json")
# Necessário para cores de logs no terminal
os.system("")

log.add_logging_level("FOLLOW", 25)
log.add_logging_level("UNFOLLOW", 26)
logger = log.get_logger()

bot = Client()
bot.set_locale("pt_BR")
bot.set_country("BRA")
bot.set_country_code(55)
bot.set_device({
            "app_version": "130.0.0.31.121",
            "android_version": 29,
            "android_release": "10",
            "dpi": "440dpi",
            "resolution": "1080x2210",
            "manufacturer": "Xiaomi",
            "device": "devluca",
            "model": "Mi 9T Pro",
            "cpu": "qcom",
            "version_code": "200396014",
        })
bot.set_user_agent("Instagram 130.0.0.31.121 Android (29/10; 440dpi; 1080x2210; Xiaomi; Mi 9T Pro; devluca; qcom; pt_BR; 200396014)")
bot.set_timezone_offset(-3 * 60 * 60)

try:
    bot.load_settings(PATH_SESSION)
    logger.info("Arquivo de sessão carregado com sucesso!")
except Exception as e:
    logger.warning(f"Erro ao ler arquivo de sessão de login. {e}")

logger.info("Iniciando login...")
bot.login(username=USERNAME, password=PASSWORD)
verificar_login(bot, PATH_SESSION)
logger.info("Login realizado com sucesso!")

contas_desejadas = ["eusoupaulinholima", "rodrigocohenoficial", "rafaelhaguiwara", "gorilakingtrader", "ojosuemendes",
                    "luizinvon", "roneyalbert_frajola", "lorenzfabricio", "papo_de_sardinha"]

counter = 1
keep_following = True
keep_unfollowing = True
retentativas_follow = 1
retentativas_unfollow = 1
while True:
    # AÇÃO FOLLOW
    sucesso_login = verificar_login(bot, PATH_SESSION, 20)
    if not sucesso_login:
        keep_following = False
        keep_unfollowing = False
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
                logger.critical(f"Desligando FOLLOW.")

    dormir(random.randint(100, 300))

    # AÇÃO UNFOLLOW
    sucesso_login = verificar_login(bot, PATH_SESSION, 20)
    if not sucesso_login:
        keep_following = False
        keep_unfollowing = False
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
                logger.critical(f"Desligando UNFOLLOW.")

    dormir(random.randint(150, 400))

    # CASO CRITICO DE ERROS
    if not keep_following and not keep_unfollowing:
        logger.critical("Algo deu errado. Parando o robô.")
        break
    counter += 1
