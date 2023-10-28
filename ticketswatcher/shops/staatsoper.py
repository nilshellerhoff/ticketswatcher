from bs4 import BeautifulSoup
from datetime import datetime
import requests

COOKIES = {
    '__cf_bm': '6fHJlyBgNzxE4vygNgvQt1Qlm_u6WIr_VQcZoAswacQ-1696436923-0-AQLwBxELlKLkAkpnsQPvinKOCDNqpK58EoJsNDpYWVDzVILPIKqhVLFPWfYv3UjaIxkL6OCVSCgcuP2P51pVuh0='
}

HEADERS = {
    # 'authority': 'www.staatsoper.de',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'accept-language': 'en-US,en;q=0.9,de;q=0.8',
    # 'cache-control': 'max-age=0',
    # # 'cookie': '__cf_bm=e9VoTXAt1A7vRWHmc3KaawG8Rny8zbtMibuP2wSNlbg-1696429560-0-AVSRh320HTwySvq3iqbtQGsww74x7hS9M1yG/56Oez4MgH9CpH9BR3KVA30H0qcfFwqyH4gVOCk3N2+RSrYTUvc=; a11y-zoom=0; a11y-contrast=0',
    # 'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Linux"',
    # 'sec-fetch-dest': 'document',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'none',
    # 'sec-fetch-user': '?1',
    # 'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
}

def getConcerts():
    # generate a list of dates e.g. 2023-10, 2023-11, 2023-12, 2024-01 ... 2024-09
    year = datetime.now().year
    month = datetime.now().month
    url_dates = [f"{year + i // 12}-{i % 12 + 1:02}" for i in range(month - 1, month + 11)]
    spielplan_urls = [f"https://www.staatsoper.de/spielplan/{year_month}" for year_month in url_dates]

    concerts = []
    for url in spielplan_urls:

        concerts.append(parse_spielplan_page(url))

    return concerts

def parse_spielplan_page(url):
    concerts = []

    r = requests.get(url, cookies=COOKIES, headers=HEADERS)
    soup = BeautifulSoup(r.text)

    for concert in soup.find_all(class_='activity-list__content'):
        date = concert.find('time')['datetime']
        concerts.append({
            'datetime': date,
            'datestr': '',
        })
