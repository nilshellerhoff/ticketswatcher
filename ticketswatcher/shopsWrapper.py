from ticketswatcher.shops import brticket, mphil, brso
from .models import Concert

def getConcerts():
    concerts = []
    concerts += getConcertsBrticket()
    concerts += getConcertsMphil()
    concerts += getConcertsBrso()
    return concerts

def getConcertsBrticket():
    return brticket.getConcerts()

def getConcertsMphil():
    return mphil.getConcerts()

def getConcertsBrso():
    return brso.getConcerts()

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
    
    return mphil.getFreeTickets(concert.ticketID)

def getTicketsBrso(concert_id):
    '''Get the details of a concert from br-so.de'''
    
    concert = Concert.objects.get(id=concert_id)
    
    if concert.ticket_url is None:
        return []
    
    return brso.getFreeTickets(concert)