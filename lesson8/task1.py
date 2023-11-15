from requests import get
from bs4 import BeautifulSoup

response = get("https://horo.mail.ru/prediction/virgo/today/")

if response.status_code != 200:
    raise Exception("Parsing failed.")

html = response.content

soup = BeautifulSoup(html, "lxml")

print("\n".join(p.text for p in soup.select("p")[:2]))
print(" ".join(span.text for span in soup.select(".p-score-day__item__value__inner")))

