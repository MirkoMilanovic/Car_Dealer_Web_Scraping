"""
The program does a web-scrapping for all of the advertisements for the used cars of the model "Smart" on the web-site:
"https://www.polovniautomobili.com/". The web-site is made for selling the used vehicles on the territory of Serbia.
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas
import math

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
r = requests.get("https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=basic&brand=smart&city_distance=0&showOldNew=all&without_price=1", headers=headers)
c = r.content
soup = BeautifulSoup(c, "html.parser")


pages_text = str(soup(text=re.compile('oglasa od ukupno'))[0])
print(pages_text)
adds_nr = int(pages_text.split("ukupno ")[1])
page_nr = math.ceil(adds_nr/25)
print(page_nr)
print(type(page_nr))


base_url = "https://www.polovniautomobili.com/auto-oglasi/pretraga?page="


l = []

for page in range(1, page_nr+1):
    r = requests.get(base_url + str(page) + "&sort=basic&brand=smart&city_distance=0&showOldNew=all&without_price=1", headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    for article in soup.find_all("article", re.compile(" uk-hidden ")):
        article.decompose()
    for article in soup.find_all("small"):
        article.decompose()
    all = soup.find_all("article", class_=re.compile("single-classified ad-"))


    for item in all:
        d = {}  # new record for one car

        d["Title"]=item.find("a", {"class": "ga-title"}).text.strip()  # car title

        try:
            d["Price"]=item.find("span", {"class": "price"}).text.replace(".", "").strip()   # price
        except:
            d["Price"]=None

        try:
            d["Old Price"]=item.find("span", {"class": "price old-price"}).text.replace(".", "").strip()   # old price
        except:
            d["Old Price"]=None

        try:
            d["Discount Price"]=item.find("span", {"class": "price price-discount"}).text.replace(".", "").strip()   # discount price
        except:
            d["Discount Price"]=None

        d["Year"]=item.find_all("div", class_=re.compile("inline-block"))[0].text.replace("|", "").replace(".", "").replace(" ", "").strip()    # year
        d["Mileage"]=item.find_all("div", class_=re.compile("inline-block"))[1].text.replace("|", "").replace("km", "").replace(" ", "").strip()   # mileage in km
        d["Fuel"]=item.find_all("div", class_=re.compile("inline-block"))[2].text.replace("|", "").replace(".", "").replace(" ", "").strip()    # fuel
        d["Engine Volume"]=item.find_all("div", class_=re.compile("inline-block"))[3].text.replace("cm3", "").replace(",", "").replace(" ", "").strip()    # engine volume cm3
        d["Car Class"]=item.find_all("div", class_=re.compile("inline-block"))[4].text.replace(",", "").replace(" ", "").strip()    # car class
        d["Engine Power"]=item.find_all("div", class_=re.compile("inline-block"))[5].text.replace(",", "").replace(" ", "").strip()    # engine power

        l.append(d)


df = pandas.DataFrame(l)
df.to_csv("Car-list-output.csv", encoding='utf8')