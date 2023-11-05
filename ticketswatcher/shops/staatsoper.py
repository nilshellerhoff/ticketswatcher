from bs4 import BeautifulSoup
from datetime import datetime
import requests
from .utils.beautifulsoup import try_get_attribute, try_get_text

COOKIES = {}

HEADERS = {
    'upgrade-insecure-requests': '1',
     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
     'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
     'sec-ch-ua-mobile': '?0',
     'sec-ch-ua-platform': '"Windows"',
     'sec-fetch-site': 'none',
     'sec-fetch-mod': '',
     'sec-fetch-user': '?1',
     'accept-encoding': 'gzip, deflate, br',
     'accept-language': 'bg-BG,bg;q=0.9,en-US;q=0.8,en;q=0.7'
}


def getConcerts():
    # generate a list of dates e.g. 2023-10, 2023-11, 2023-12, 2024-01 ... 2024-09
    year = datetime.now().year
    month = datetime.now().month
    url_dates = [f"{year + i // 12}-{i % 12 + 1:02}" for i in range(month - 1, month + 11)]
    spielplan_urls = [f"https://www.staatsoper.de/spielplan/{year_month}/calendar.ajax" for year_month in url_dates]

    concerts = []
    for url in spielplan_urls:
        print(f"fetching concerts from {url}")
        concerts += parse_spielplan_page(url)

    return concerts

def parse_spielplan_page(url):
    concerts = []

    r = requests.get(url, cookies=COOKIES, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    for concert in soup.find_all(class_='activity-list__row'):
        if "In diesem Zeitraum gibt es keine Vorstellungen" in concert.select_one('h3').text:
            continue

        date = try_get_attribute(concert, 'time', 'datetime')
        title = try_get_text(concert, '.activity-list__text h3')

        time, location, *_ = try_get_text(concert, '.activity-list__text span').split('|')
        date_time = datetime.strptime(date + ' ' + time.strip(), '%Y-%m-%d %H.%M Uhr')
        venue = location.strip()

        base_url = 'https://staatsoper.de'
        url = base_url + try_get_attribute(concert, '.activity-list__content', 'href')
        ticket_url = try_get_attribute(concert, '.activity-list__col--tickets .button--ticket', 'href')

        category = try_get_text(concert, '.activity-list__col--genre').strip()

        concerts.append({
            'provider': 'staatsoper',
            'title': title.strip(),
            'details': try_get_text(concert, '.activity-list--toggle__content'),
            'category': category,
            'datestr': '',
            'datetime': date_time,
            'image': '',
            'url': url,
            'ticketID': '',
            'ticket_url': ticket_url,
            'venue': venue,
        })

    return concerts


if __name__ == '__main__':
    print(getConcerts())