from datetime import datetime

from django.db.models import Sum
from django.core.mail import send_mail

from . import shopsWrapper
from .models import Concert, Ticket, TicketReductionType, Watcher

FROM_EMAIL: str = 'ticketswatcher@forelleh.de'

def loadConcerts():
    """Load concerts from the website into the DB"""
    concerts = shopsWrapper.getConcerts()

    for concert in concerts:
        Concert.objects.update_or_create(
            **{
                'title': concert['title'],
                'datestr': concert['datestr'],
            }, defaults={
                'details': concert.get('details'),
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
            }, defaults={
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

    # only future concerts
    watchers_to_be_checked = Watcher.objects.filter(concert__datetime__gte=datetime.date(datetime.now()))

    for watcher in watchers_to_be_checked:
        try:
            loadTickets(watcher.concert_id)

            concert = Concert.objects.get(pk=watcher.concert_id)

            filters = {
                "concert_id": watcher.concert_id,
            }

            if watcher.max_price > 0:
                filters["price__lte"] = watcher.max_price

            if watcher.types.all():
                filters["reduction_type__in"]: watcher.types.all()

            tickets = Ticket.objects.filter(**filters)

            tickets_available = tickets.aggregate(Sum('available'))['available__sum'] or 0

            if tickets_available > 0 and tickets_available > watcher.num_tickets:
                print(f"Found {tickets_available} tickets for watcher {watcher.email}!")

                body_str = ""
                body_str += f"Found {tickets_available} tickets for concert {concert.title} on {concert.datestr}!"
                body_str += "\n\n"
                body_str += "\n".join(
                    [f"{ticket.available}x {ticket.category} {ticket.price}€ {ticket.name}" for ticket in tickets if
                     ticket.available > 0])
                body_str += "\n\n"
                body_str += f"Check out the tickets here: {concert.ticket_url}"
                body_str += "\n\n"
                body_str += "This is an automated email from ticketswatcher. Remove this watcher by clicking on the link below.\n"
                body_str += f"http://ticketswatcher.forelleh.de/deleteWatcher/{watcher.uuid}"

                send_mail(
                    'Ticketswatcher found tickets',
                    body_str,
                    FROM_EMAIL,
                    [watcher.email],
                    fail_silently=False,
                )
            else:
                print(f"No tickets found for watcher {watcher.email}!")
        except:
            print(f"error checking watcher {watcher.uuid}")


def sendTestEmail(recipient="nils.hellerhoff@gmail.com"):
    """send a test email to the admin"""
    send_mail(
        'Ticketswatcher test email',
        'This is a test email from ticketswatcher',
        FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
