from bs4 import BeautifulSoup

with open("Сайт. Заповедники/html/beresinskiy.html", "r", encoding="UTF-8") as fl:
    html = fl.read()

soup = BeautifulSoup(html, "lxml")
paragraphs = soup.select("p")

for p in paragraphs:
    print(p.text.replace("  ", "").strip())
    print()
