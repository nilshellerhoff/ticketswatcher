import requests
from bs4 import BeautifulSoup
import datetime

def getConcerts() -> list:
    '''Get all the listed concerts from musikverein.at'''

    concerts = []

    url = 'https://www.mphil.de/konzerte-karten/kalender'

    r = requests.get(url)

    if r.status_code != 200:
        raise Exception('Error while fetching concerts from mphil.de')

    soup = BeautifulSoup(r.text, 'html.parser')

    return _parsePage(soup)


def _parsePage(soup: BeautifulSoup) -> list:
    '''Parse the html of a page of mphil.de'''

    concerts = []

    for concert in soup.select('li.mp16_cal-listitem'):
        c = {}

        c['provider'] = 'mphil'
        c['title'] = concert.select_one('h2.thetitles').text.strip().replace("\n", " ").replace("\t", "")
        c['datestr'] = concert.select_one('time.concert__date').text.strip()
        c['datetime'] = _parseDate(c['datestr'])

        try:
            c['ticketID'] = concert.select_one('ticket-button')['identifier']
        except:
            c['ticketID'] = None
        
        try:
            c['image'] = concert.select_one('figure.card__image img')['src']
        except:
            c['image'] = None
        
        try: c['url'] = _getFullUrl(concert.select_one('div.concert__buttons a.opas-detail-link')['href'])
        except: c['url'] = None

        try:
            c['ticket_url'] = _getFullUrl(concert.select_one('ticket-button a')['href'])
        except:
            c['ticket_url'] = None

        c['venue'] = concert.select_one('div.concert__venue').text.strip()
        
        concerts.append(c)
        
    return concerts

def _getFullUrl(url: str) -> str:
    '''Get the full url of a link on mphil.de'''

    if url.startswith('/'):
        return f'https://www.mphil.de{url}'
    else:
        return url
        

def _parseDate(datestr: str) -> str:
    '''Parse the date of a concert from mphil.de and return it in the format YYYY-MM-DDT00:00:00
    Format on page is like this: Sonntag, 18.12.2022, 11 Uhr or Donnerstag, 02.02.2023, 18.30 Uhr'''

    date = datestr.split(', ')[1]
    time = datestr.split(', ')[2].split(" ")[0]
    
    day = int(date.split('.')[0])
    month = int(date.split('.')[1])
    year = int(date.split('.')[2])

    # check if time is given in format 11 Uhr or 18.30 Uhr
    if "." in time:
        hour = int(time.split('.')[0])
        minute = int(time.split('.')[1])
    else:
        hour = int(time.split(':')[0])
        minute = 0
    
    seconds = 0

    # this works as long as the locale is set to german
    return datetime.datetime(year, month, day, hour, minute, seconds).isoformat()

def getFreeTickets(concert_api_id):
    '''Get the details of a concert from mphil.de'''
    
    api_url = f"https://darjayf5vzuub.cloudfront.net/api/system/s5fkpivanrzu/seat-selection/booking-info/20221215152315/{concert_api_id}"

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