from utils.bot_config import InstagramBot
from utils import actions
import os
import glob
from utils import log

logger = log.get_logger()

try:
    cookie_del = glob.glob("config/*cookie.json")
    os.remove(cookie_del[0])
except Exception as e:
    logger.error(f"Erro ao excluir cookies {e}")

bot = InstagramBot(max_follows_per_day=200, max_unfollows_per_day=200)

bot.login(username=os.environ['username'], password=os.environ['password'])
contas_desejadas = ["eusoupaulinholima", "rodrigocohenoficial", "rafaelhaguiwara"]

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
            logger.warning(f"Ação FOLLOW finalizada com sucesso na {counter}ª vez.")
        else:
            if retentativas_follow < 2:
                retentativas_follow += 1
                logger.error(f"Ação FOLLOW finalizada com erro na {counter}ª vez. Irá tentar novamente...")
            else:
                keep_following = False
                logger.critical(f"Ação FOLLOW finalizada com erro na {counter}ª vez.")
                logger.critical(f"Número de retentativas excedido para FOLLOW. Desligando FOLLOW.")
    # AÇÃO UNFOLLOW
    if keep_unfollowing:
        sucesso = actions.unfollow(bot)
        if sucesso:
            retentativas_unfollow = 1
            logger.warning(f"Ação UNFOLLOW finalizada com sucesso na {counter}ª vez.")
        else:
            if retentativas_unfollow < 2:
                retentativas_unfollow += 1
                logger.error(f"Ação UNFOLLOW finalizada com erro na {counter}ª vez. Irá tentar novamente...")
            else:
                keep_unfollowing = False
                logger.critical(f"Ação UNFOLLOW finalizada com erro na {counter}ª vez.")
                logger.critical(f"Número de retentativas excedido para UNFOLLOW. Desligando UNFOLLOW.")
    if not keep_following and not keep_unfollowing:
        logger.critical("Algo deu errado. Parando o robô.")
        break
    counter += 1
