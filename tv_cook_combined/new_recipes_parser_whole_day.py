from db import DB
from parser import CookParser
from proxy_cheker import check
from time import sleep

with open("proxies.txt") as fl:
    proxies = fl.read().splitlines()

db = DB("cooking.db")

while True:
    parser = CookParser(check(proxies))
    parser.parse_category("Главная страница", db_object=db)
    sleep(60 * 6)
