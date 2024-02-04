from datetime import datetime
from typing import List

from django.db.models import Sum
from django.core.mail import send_mail

from . import shopsWrapper
from .models import Concert, Ticket, TicketReductionType, Watcher

FROM_EMAIL: str = 'ticketswatcher@forelleh.de'

def loadConcerts():
    """Load concerts from the website into the DB"""
    concerts = shopsWrapper.getConcerts()

    for concert in concerts:
        try:
            Concert.objects.update_or_create(
                **{
                    'title': concert['title'],
                    'datestr': concert['datestr'],
                    'datetime': concert['datetime'],
                }, defaults={
                    'details': concert.get('details'),
                    'provider': concert['provider'],
                    'datetime': concert['datetime'],
                    'ticketID': concert['ticketID'],
                    'image': concert['image'],
                    'url': concert['url'],
                    'ticket_url': concert['ticket_url'],
                    'venue': concert['venue'],
                    'last_updated': datetime.now(),
                }
            )
        except Exception as e:
            print(f"Error updating concert {concert['title']}: {str(e)}")

    return len(concerts)


def load_tickets(concert_id: int):
    """Load tickets from the website into the DB"""

    try:
        concert = Concert.objects.get(pk=concert_id)
    except Concert.DoesNotExist:
        return 0

    try:
        tickets = shopsWrapper.getTickets(concert.id)

        # delete all ticket entries
        Ticket.objects.filter(concert_id=concert.id).delete()

        for ticket in tickets:
            TicketReductionType.objects.update_or_create(name=ticket['name'])

            # create new ticket entries
            if ticket['identifier']:
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
            else:
                Ticket.objects.update_or_create(
                    **{
                        'concert_id': concert.id,
                        'category': ticket['category'],
                        'name': ticket['name'],
                    }, defaults={
                        'identifier': ticket['identifier'],
                        'sort': ticket['sort'],
                        'price': ticket['price'],
                        'color': ticket['color'],
                        'available': ticket['available'],
                        'reduction_type': TicketReductionType.objects.get(name=ticket['name']),
                    }
                )

        # finally update concert last ticket update field
        concert.last_ticket_updated = datetime.now()
        concert.save()

        return len(tickets)
    except Exception as e:
        print(f"{str(e)}")
        return 0


def check_watchers() -> None:
    """Load tickets and check if any tickets are available for watchers"""

    # only future concerts
    watchers_to_be_checked = Watcher.objects.filter(concert__datetime__gte=datetime.date(datetime.now()))

    for watcher in watchers_to_be_checked:
        try:
            check_watcher(watcher)
        except:
            print(f"error checking watcher {watcher.uuid}")


def check_watcher(watcher: Watcher) -> None:

    load_tickets(watcher.concert_id)

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

    old_availability = watcher.available

    if tickets_available > 0 and tickets_available > watcher.num_tickets:
        watcher.available = True

        # we only send mail if the status has changed from unavailable to available
        if not old_availability:
            print(f"Found {tickets_available} tickets for watcher {watcher.email}, sending mail!")
            send_ticket_mail(watcher, concert, tickets, tickets_available)
        else:
            print(f"Found {tickets_available} tickets for watcher {watcher.email}, not sending mail!")

    else:
        print(f"No tickets found for watcher {watcher.email}!")
        watcher.available = False

    watcher.save()


def send_ticket_mail(watcher: Watcher, concert: Concert, tickets: List[Ticket], tickets_available: int):
    """send the ticket available mail

    Parameters:
        watcher: the watcher object
        concert: the concert object of the watcher
        tickets: the available tickets for the watcher
        tickets_available: the number of tickets available
    """
    current_host = "http://ticketswatcher.forelleh.de"

    ticket_table_row = "{ticket.available}x {ticket.category} {ticket.price}€ {ticket.name}"

    ticket_table_str = "\n".join([ticket_table_row.format(ticket=t) for t in tickets if t.available > 0])

    body_str = f"""
Found {tickets_available} tickets for concert {concert.title} on {concert.datestr}!

{ticket_table_str}

Check out the tickets here: {current_host}/concert/{watcher.concert_id}

This is an automated email from ticketswatcher.
You can manage your watchers here: {current_host}/watchers?email={watcher.email} 
or remove this watcher directly with the following url: {current_host}/deleteWatcher/{watcher.uuid}"""

    send_mail(
        'Ticketswatcher found tickets',
        body_str,
        FROM_EMAIL,
        [watcher.email],
        fail_silently=False,
    )


def sendTestEmail(recipient="nils.hellerhoff@gmail.com"):
    """send a test email to the admin"""
    send_mail(
        'Ticketswatcher test email',
        'This is a test email from ticketswatcher',
        FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
