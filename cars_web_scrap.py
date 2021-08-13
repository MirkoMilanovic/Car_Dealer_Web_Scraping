"""
The program does a web-scrapping for all of the advertisements of the cars on the web-site:
"https://www.polovniautomobili.com/"
"""
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
r = requests.get("https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=basic&city_distance=0&showOldNew=all&without_price=1", headers=headers)
c = r.content
soup = BeautifulSoup(c, "html.parser")
for article in soup.find_all("article", re.compile(" uk-hidden ")):
    article.decompose()
for article in soup.find_all("small"):
    article.decompose()
all = soup.find_all("article", class_=re.compile("single-classified ad-"))


for item in all:
    print(item.find("a", {"class": "ga-title"}).text.strip())  # print the car title

    try:
        print(item.find("span", {"class": "price"}).text.strip())   # price
    except:
        print(None)

    try:
        print(item.find("span", {"class": "price old-price"}).text.strip())   # old price
    except:
        print(None)

    try:
        print(item.find("span", {"class": "price price-discount"}).text.strip())   # discount price
    except:
        print(None)

    print(item.find_all("div", class_=re.compile("inline-block"))[0].text.replace("|", "").replace(".", "").replace(" ", "").strip())    # year
    print(item.find_all("div", class_=re.compile("inline-block"))[1].text.replace("|", "").replace("km", "").replace(" ", "").strip())   # mileage in km
    print(item.find_all("div", class_=re.compile("inline-block"))[2].text.replace("|", "").replace(".", "").replace(" ", "").strip())    # fuel
    print(item.find_all("div", class_=re.compile("inline-block"))[3].text.replace("cm3", "").replace(",", "").replace(" ", "").strip())    # engine volume cm3
    print(item.find_all("div", class_=re.compile("inline-block"))[4].text.replace(",", "").replace(" ", "").strip())    # car class
    print(item.find_all("div", class_=re.compile("inline-block"))[5].text.replace(",", "").replace(" ", "").strip())    # engine power

    print("\n")
