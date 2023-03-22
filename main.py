from instabot import Bot
import random
from utils import actions
import os
import glob
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')

try:
    cookie_del = glob.glob("config/*cookie.json")
    os.remove(cookie_del[0])
except Exception as e:
    logger.error(f"Erro ao excluir cookies {e}")

bot = Bot()

# Sobrescrevendo configurações do robô
bot.delays["follow"] = random.randint(200, 400)
bot.max_follows_per_day = 200
bot.max_unfollows_per_day = 200
bot.logger.setLevel("ERROR")

bot.login(username=os.environ['username'], password=os.environ['password'])
contas_desejadas = ["eusoupaulinholima", "rodrigocohenoficial", "canal.contareal"]


def verificar_sucesso_acoes(verificador, nome_acao, counter):
    if verificador:
        logger.info(f"Ação {nome_acao} finalizada com sucesso pela {counter}ª vez.")
    else:
        logger.error(f"Ação {nome_acao} finalizada com erro na {counter}ª vez.")


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
        logger.error("Algo deu errado. Parando o robô.")
        break
    counter += 1
