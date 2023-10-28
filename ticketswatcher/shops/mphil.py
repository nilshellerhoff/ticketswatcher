## module for mphil.de

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .utils import muenchenticket
from .utils.beautifulsoup import try_get_attribute, try_get_text
from .utils.formatting import oneline
from ..models import Concert

def getConcerts() -> list:
    '''Get all the listed concerts from mphil.de'''

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

    concert_list = soup.select('.m-mphil-concertlist__item')

    for concert in concert_list:
        c = {}

        c['provider'] = 'mphil'
        c['title'] = oneline(concert.select_one('h2.m-mphil-concertlist__headline').text)
        c['datestr'] = concert.select_one('time.m-mphil-concertlist__date').text.strip()

        datetime_iso = concert.select_one('time.m-mphil-concertlist__date')["datetime"]
        c['datetime'] = datetime.strptime(datetime_iso, "%Y-%m-%d %H:%M")

        c['worklist'] = try_get_text(concert, '.m-mphil-concertlist__work-list')
        c['performers'] = try_get_text(concert, '.m-mphil-concertlist__person-list')

        c['image'] = try_get_attribute(concert, 'figure img', 'src')

        _url = try_get_attribute(concert, '.m-mphil-concertlist__detail-link', 'href')
        c['url'] = _getFullUrl(_url) if _url else None

        # doesn't exist right now, could be constructed though probably
        c['ticket_url'] = None
        c['ticketID'] = try_get_attribute(concert, 'ticket-button', 'identifier')

        c['venue'] = try_get_text(concert, '.m-mphil-concertlist__venue')
        
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
    return datetime(year, month, day, hour, minute, seconds).isoformat()

def getFreeTickets(concert: Concert):
    api_base_url = "https://darjayf5vzuub.cloudfront.net/api/system/s5fkpivanrzu/seat-selection/booking-info/20221215152315"
    return muenchenticket.get_free_tickets(concert.ticketID, base_url=api_base_url)
