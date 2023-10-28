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
    if "brticket" in ENABLED_SHOPS:
        concerts += brticket.getConcerts()
    if "mphil" in ENABLED_SHOPS:
        concerts += mphil.getConcerts()
    if "brso" in ENABLED_SHOPS:
        concerts += brso.getConcerts()
    if "staatsoper" in ENABLED_SHOPS:
        concerts += staatsoper.getConcerts()
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