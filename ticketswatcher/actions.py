from django.db.models import Sum
from django.core.mail import send_mail

from . import shopsWrapper
from .models import Concert, Ticket, TicketReductionType, Watcher

def loadConcerts():
    """Load concerts from the website into the DB"""
    concerts = shopsWrapper.getConcerts()

    for concert in concerts:
        Concert.objects.update_or_create(
            **{
                'title': concert['title'],
                'datestr': concert['datestr'],
            }, defaults = {
                'provider': concert['provider'],
                'datetime': concert['datetime'],
                'ticketID': concert['ticketID'],
                'image': concert['image'],
                'url': concert['url'],
                'ticket_url': concert['ticket_url'],
                'venue': concert['venue'],
            }
        )
    
    return len(concerts)

def loadTickets(concert_id: int):
    """Load tickets from the website into the DB"""

    try:
        concert = Concert.objects.get(pk=concert_id)
    except Concert.DoesNotExist:
        return 0

    tickets = shopsWrapper.getTickets(concert.id)

    # delete all ticket entries
    Ticket.objects.filter(concert_id=concert.id).delete()

    for ticket in tickets:
        TicketReductionType.objects.update_or_create(name=ticket['name'])


        # create new ticket entries
        Ticket.objects.update_or_create(
            **{
                'concert_id': concert.id,
                'identifier': ticket['identifier'],
            }, defaults = {
                'sort': ticket['sort'],
                'category': ticket['category'],
                'price': ticket['price'],
                'name': ticket['name'],
                'color': ticket['color'],
                'available': ticket['available'],
                'reduction_type': TicketReductionType.objects.get(name=ticket['name']),
            }
        )

    
    return len(tickets)

def checkWatchers():
    """Load tickets and check if any tickets are available for watchers"""

    for watcher in Watcher.objects.all():
        loadTickets(watcher.concert_id)
        tickets = Ticket.objects.filter(
            concert_id=watcher.concert_id,
            price__lte=watcher.max_price,
            reduction_type__in=watcher.types.all())

        if tickets.count() > watcher.num_tickets:
            print(f"Found {tickets.aggregate(Sum('available'))} tickets for watcher {watcher.email}!")
        else:
            print(f"No tickets found for watcher {watcher.email}!")

def sendTestMail():
    """send a test email to the admin"""
    send_mail(
        'Ticketswatcher test email',
        'This is a test email from ticketswatcher',
        'ticketswatcher@ticketswatcher.forelleh.de',
        ['nils.hellerhoff@gmail.com'],
        fail_silently=False,
    )