from ticketswatcher.shops import brticket, mphil, brso, staatsoper
from .models import Concert

ENABLED_SHOPS = [
    "mphil",
    "brso",
    "brticket",
    # "staatsoper",
]

def getConcerts():
    concerts = []

    for shop in ENABLED_SHOPS:
        concerts += load_concerts(shop)

    return concerts


def load_concerts(shopname: str):
    try:
        print(f"loading concerts for {shopname}")
        concerts = eval(f"{shopname}.getConcerts()")
        print(f"{len(concerts)} concerts loaded")
    except Exception as e:
        print(f"failed to load concerts for {shopname}, {str(e)}")
        return []

    return concerts

def getConcertsBrticket():
    return brticket.getConcerts()

def getConcertsMphil():
    return mphil.getConcerts()

def getConcertsBrso():
    return brso.getConcerts()

def getConcertsStaatsoper():
    return staatsoper.getConcerts()

def getTickets(concert_id):
    '''Get the details of a concert from all providers'''

    concert = Concert.objects.get(id=concert_id)
    if concert.provider == 'brticket':
        return getTicketsBrticket(concert_id)
    elif concert.provider == 'mphil':
        return getTicketsMphil(concert_id)
    elif concert.provider == 'brso':
        return getTicketsBrso(concert_id)
    elif concert.provider == 'staatsoper':
        return getTicketsStaatsoper(concert_id)
    else:
        raise Exception('Unknown provider')


def getTicketsBrticket(concert_id):
    '''Get the details of a concert from br-ticket.de'''

    concert = Concert.objects.get(id=concert_id)
    
    if concert.ticketID is None:
        return []
    
    return brticket.getFreeTickets(concert.ticketID)

def getTicketsMphil(concert_id):
    '''Get the details of a concert from mphil.de'''
    
    concert = Concert.objects.get(id=concert_id)
    
    if concert.ticketID is None:
        return []

    return mphil.getFreeTickets(concert)

def getTicketsBrso(concert_id):
    '''Get the details of a concert from br-so.de'''
    
    concert = Concert.objects.get(id=concert_id)
    
    if concert.ticket_url is None:
        return []
    
    return brso.getFreeTickets(concert)


def getTicketsStaatsoper(concert_id: int):
    concert = Concert.objects.get(id=concert_id)

    if concert.ticket_url is None:
        return []

    return staatsoper.getFreeTickets(concert)