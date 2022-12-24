## module for br-so.de

import requests
from math import ceil
from bs4 import BeautifulSoup
import datetime
from typing import Union

def getConcerts():
    '''Get all the listed concerts from br-so.de'''

    url = "https://www.br-so.de/konzerte/konzert-kalender/"

    r = requests.get(url)

    if r.status_code != 200:
        raise Exception('Error while fetching concerts from br-so.de')
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        concerts = _parsePage(soup)

    return concerts

def _parsePage(soup: BeautifulSoup) -> list:
    '''Parse the html of a page of br-ticket.de'''

    concerts = []

    for concert in soup.select('li.konzertteaser'):
        c = {}

        c['provider'] = 'brso'
        c['title'] = concert.select_one('div.info h6').text.strip()

        d = concert.select_one('div.date d').text.strip()
        m = concert.select_one('div.date m').text.strip()
        y = concert.select_one('div.date y').text.strip()

        c['datestr'] = f"{d} {m} {y}"
        c['datetime'] = "" # _parseDate(c['datestr'])
        
        c["ticketID"] = None

        c['image'] = None

        try:
            c['url'] = _getFullUrl(concert.select_one('a.btn.programmpreview')['href'])
        except:
            c['url'] = None
        
        try:
            c['ticket_url'] = _getFullUrl(concert.select_one('a.btn.cart')['href'])
        except:
            c['ticket_url'] = None
        
        c['venue'] = concert.select_one('div.info p').text.strip()

        concerts.append(c)
        
    return concerts

def _getFullUrl(url: str) -> str:
    '''Get the full url of a link on mphil.de'''

    if url.startswith('/'):
        return f'https://www.br-so.de{url}'
    else:
        return url


def _parseDate(datestr: str) -> str:
    '''Parse the date of a concert from br-so.de and return it in the format YYYY-MM-DDT00:00:00'''

    date = datestr.split(', ')[1]
    time = datestr.split(', ')[2]
    
    day = int(date.split('.')[0])
    month = int(date.split('.')[1])
    year = int(date.split('.')[2]) + 2000

    hour = int(time.split(':')[0])
    minute = int(time.split(':')[1])
    seconds = 0

    # this works as long as the locale is set to german
    return datetime.datetime(year, month, day, hour, minute, seconds).isoformat()

def getFreeTickets(concert_api_id):
    '''Get the details of a concert from br-ticket.de'''
    
    api_url = f"https://darjayf5vzuub.cloudfront.net/api/system/stbhl30h6k9a/seat-selection/booking-info/20221214135045/{concert_api_id}"

    r = requests.get(api_url)

    if r.status_code != 200:
        raise Exception('Error while fetching concert details from br-ticket.de')
    
    prices = []

    for price in r.json()['prices']:
        p = {}
        p['identifier'] = price['identifier']
        p['category'] = price['name']
        p['sort'] = price['sortPosition']
        p['name'] = price['priceName']
        p['color'] = price['hexColor']
        p['price'] = price['amount']
        p['available'] = price['maxAllowedTickets']
        prices.append(p)

        if 'reductions' in price.keys():
            for price2 in price['reductions']:
                p2 = {}
                p2['identifier'] = price2['identifier']
                p2['category'] = price['name']
                p2['sort'] = price['sortPosition']
                p2['name'] = price2['name']
                p2['color'] = price['hexColor']
                p2['price'] = price2['amount']
                p2['available'] = price2['maxAllowedTickets']
                prices.append(p2)

    return prices