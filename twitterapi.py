# -*- coding: utf-8 -*-

import os
from datetime import datetime
import re
import sqlite3
from urllib.request import urlopen
from html import unescape
import requests
import twitter




def main():
    html = fetch('https://jpbitcoin.com/markets')
    #print(html)
    scrape(html)
    bitcoin = scrape(html)
    maxp = 0
    minp = 10000000
    buypl = ""
    sellpl = ""
    for i in range(6):
        buytem = bitcoin[i]['buy']
        selltem = bitcoin[i]['sell']
        if buytem < minp:
            minp = buytem
            buypl = bitcoin[i]['place']
        if selltem > maxp:
            maxp = selltem
            sellpl = bitcoin[i]['place']

    maxdiff = maxp - minp
    print('maxdiff:{0}, sellplace:{1}, buyplace:{2}!'.format(maxdiff,sellpl,buypl))

    api = twitter.Api(consumer_key=os.environ["CONSUMER_KEY"],
                      consumer_secret=os.environ["CONSUMER_SECRET"],
                      access_token_key=os.environ["ACCESS_TOKEN_KEY"],
                      access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
                      )



    if maxdiff>100:
            api.PostUpdate('maxdiff:{0}, sellplace:{1}, buyplace:{2}!'.format(maxdiff,sellpl,buypl))




def fetch(url):
    r = requests.get(url)
    html = r.text
    return html

def scrape(html):
    bitcoin=[]
    for partial_html in re.findall(r'<a href="https://.{,50}<img src=".{,200}</tr>', html, re.DOTALL)[:7]:
        place = re.search(r'\.png">(.*?)</a>', partial_html).group(1)
        if place == 'Kraken':
            continue
        maxprice = int(re.findall(r'<td>([0-9]*)<\/td>', partial_html,re.IGNORECASE)[1])
        minprice = int(re.findall(r'<td>([0-9]*)<\/td>', partial_html,re.IGNORECASE)[0])
        bitcoin.append({'place': place, 'buy': maxprice, 'sell': minprice})
    return bitcoin


main()
