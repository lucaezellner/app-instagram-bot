from utils.bot_config import InstagramBot
from utils import actions
import os
import glob
from utils import log
from dotenv import load_dotenv

load_dotenv()

log.add_logging_level("FOLLOW", 25)
log.add_logging_level("UNFOLLOW", 26)
logger = log.get_logger()

try:
    cookie_del = glob.glob("config/*cookie.json")
    os.remove(cookie_del[0])
except Exception as e:
    logger.error(f"Erro ao excluir cookies {e}")

bot = InstagramBot(max_follows_per_day=200, max_unfollows_per_day=600)

bot.login(username=os.environ['usuario'], password=os.environ['senha'])
contas_desejadas = ["eusoupaulinholima", "rodrigocohenoficial", "rafaelhaguiwara"]

counter = 1
keep_following = True
keep_unfollowing = True
retentativas_follow = 1
retentativas_unfollow = 1
while True:
    bot.print_counters()
    # AÇÃO FOLLOW
    if keep_following and (counter % 2 == 0):
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
    if not keep_following and not keep_unfollowing:
        logger.critical("Algo deu errado. Parando o robô.")
        break
    counter += 1
