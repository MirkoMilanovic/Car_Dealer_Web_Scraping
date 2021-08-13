"""
The program does a web-scrapping for all of the advertisements of the cars on the web-site:
"https://www.polovniautomobili.com/"
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas

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


l = []

for item in all:
    d = {}  # new record for one car

    d["Title"]=item.find("a", {"class": "ga-title"}).text.strip()  # car title

    try:
        d["Price"]=item.find("span", {"class": "price"}).text.strip()   # price
    except:
        d["Price"]=None

    try:
        d["Old Price"]=item.find("span", {"class": "price old-price"}).text.strip()   # old price
    except:
        d["Old Price"]=None

    try:
        d["Discount Price"]=item.find("span", {"class": "price price-discount"}).text.strip()   # discount price
    except:
        d["Discount Price"]=None

    d["Year"]=item.find_all("div", class_=re.compile("inline-block"))[0].text.replace("|", "").replace(".", "").replace(" ", "").strip()    # year
    d["Mileage"]=item.find_all("div", class_=re.compile("inline-block"))[1].text.replace("|", "").replace("km", "").replace(" ", "").strip()   # mileage in km
    d["Fuel"]=item.find_all("div", class_=re.compile("inline-block"))[2].text.replace("|", "").replace(".", "").replace(" ", "").strip()    # fuel
    d["Engine Volume"]=item.find_all("div", class_=re.compile("inline-block"))[3].text.replace("cm3", "").replace(",", "").replace(" ", "").strip()    # engine volume cm3
    d["Car Class"]=item.find_all("div", class_=re.compile("inline-block"))[4].text.replace(",", "").replace(" ", "").strip()    # car class
    d["Engine Power"]=item.find_all("div", class_=re.compile("inline-block"))[5].text.replace(",", "").replace(" ", "").strip()    # engine power

    l.append(d)


print(l)
print(len(l))

df = pandas.DataFrame(l)
print(df)
df.to_csv("Car-list-output.csv", encoding='utf8')