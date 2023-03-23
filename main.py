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


def verificar_sucesso_acoes(verificador, nome_acao, counter):
    if verificador:
        logger.warning(f"Ação {nome_acao} finalizada com sucesso pela {counter}ª vez.")
    else:
        logger.critical(f"Ação {nome_acao} finalizada com erro na {counter}ª vez.")


counter = 1
keep_following = True
keep_unfollowing = True
while True:
    if keep_following:
        keep_following = actions.follow(bot, contas_desejadas)
        verificar_sucesso_acoes(keep_following, "FOLLOW", counter)
    if keep_unfollowing:
        keep_unfollowing = actions.unfollow(bot)
        verificar_sucesso_acoes(keep_unfollowing, "UNFOLLOW", counter)
    if not keep_following and not keep_unfollowing:
        logger.critical("Algo deu errado. Parando o robô.")
        break
    counter += 1
