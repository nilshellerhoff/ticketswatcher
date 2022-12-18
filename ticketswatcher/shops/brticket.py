## module for br-ticket.de
 
import requests
from math import ceil
from bs4 import BeautifulSoup
import datetime
from typing import Union

def getConcerts(numMax = None) -> list:
    '''Get all the listed concerts from br-ticket.de'''

    concerts = _getConcerts(maxNum=numMax)

    return concerts

def _getConcerts(maxNum: Union[int,None] = None) -> list:
    '''Get the api IDs of all the listed concerts from br-ticket.de'''

    concertsPerPage = 10
    pagesToFetch = ceil(maxNum / concertsPerPage) if maxNum is not None else None

    concerts = []

    pageNum = 1
    while pagesToFetch is None or pageNum <= pagesToFetch:
        url = f'https://www.br-ticket.de/events/page/{pageNum}/?filter=0'

        print(f'Fetching concerts from {url}...')

        r = requests.get(url)
        if r.status_code == 404:
            # no more pages
            return concerts

        if r.status_code != 200:
            raise Exception('Error while fetching concerts from br-ticket.de')

        soup = BeautifulSoup(r.text, 'html.parser')

        concerts += _parsePage(soup)

        pageNum += 1

    return concerts

def _parsePage(soup: BeautifulSoup) -> list:
    '''Parse the html of a page of br-ticket.de'''

    concerts = []

    for concert in soup.select('div.events__item'):
        c = {}

        c['provider'] = 'brticket'
        c['title'] = concert.select_one('div.event__info h3 a').text.strip()
        c['datestr'] = concert.select_one('div.event__info p.event__date-full').text.strip()
        c['datetime'] = _parseDate(c['datestr'])
        try:
            c['ticketID'] = concert.select_one('ticket-button')['identifier']
        except:
            c['ticketID'] = None
        
        try:
            c['image'] = concert.select_one('div.event__image img')['src']
        except:
            c['image'] = None
        try: c['url'] = concert.select_one('div.event__text a')['href']
        except: c['url'] = None
        c['ticket_url'] = concert.select_one('div.event__info h3 a')['href']

        c['venue'] = concert.select_one('div.event__info p.event__place').text.strip()

        concerts.append(c)
        
    return concerts

def _parseDate(datestr: str) -> str:
    '''Parse the date of a concert from br-ticket.de and return it in the format YYYY-MM-DDT00:00:00'''

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