import requests

API_BASE_URL = "https://darjayf5vzuub.cloudfront.net/api/de/system/stbhl30h6k9a/seat-selection/booking-info/20231001173200"
def get_free_tickets(concert_api_id, base_url = None):
    '''Get the details of a concert from mphil.de'''

    if not concert_api_id:
        return []

    if not base_url:
        base_url = API_BASE_URL

    api_url = f"{base_url}/{concert_api_id}"

    r = requests.get(api_url)

    if r.status_code != 200:
        raise Exception('Error while fetching concert details')

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