from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse

from .models import Concert, Ticket, TicketReductionType, Watcher

from . import actions

from datetime import datetime, timedelta

import json
import uuid
from django.core import serializers

def index(request):
    concerts = Concert.objects.filter(datetime__gte = datetime.date(datetime.now())).order_by('datetime')
    concerts_json = serializers.serialize("json", concerts)

    # adding ticket info (yes this is stupid)
    output = json.loads(concerts_json)
    for entry in output:
        concert = Concert.objects.get(id=entry["pk"])
        entry["fields"]["available_tickets"] = concert.available_tickets
    concerts_json = json.dumps(output)

    return render(request, 'ticketswatcher/index.html', {'concerts': concerts_json})


def watchers(request):
    email = request.GET.get("email")
    watchers = Watcher.objects.filter(email=email, concert__datetime__gte=datetime.date(datetime.now())).order_by('concert__datetime')
    context = {
        'watchers' : watchers,
        'email': email
    }
    return render(request, 'ticketswatcher/watchers.html', context)

def concert(request, concert_id):
    watcher_id = request.GET.get("watcher_id")
    watcher, watcher_status = None, None

    if watcher_id:
        try:
            watcher_status = "success"
            watcher = Watcher.objects.get(uuid=watcher_id)
        except:
            watcher_status = "error"

    concert = get_object_or_404(Concert, pk=concert_id)

    actions.loadTickets(concert_id)
    tickets = Ticket.objects.filter(concert_id=concert_id).order_by('sort', '-price')
    ticket_types = Ticket.objects.filter(concert_id=concert_id).values('reduction_type__name', 'reduction_type__id').distinct()


    return render(request, 'ticketswatcher/concert.html', {
        'concert': concert,
        'tickets': tickets,
        'ticket_types': ticket_types,
        'watcher_status': watcher_status,
        'watcher': watcher
    })

def watch(request, concert_id):

    concert = get_object_or_404(Concert, pk=concert_id)

    watcher = Watcher()

    watcher.concert = concert

    ticket_types = []

    for key in request.POST.keys():
        if key.startswith('ticket_type_'):
            ticket_type_id = int(key.split('_')[2])
            ticket_types.append(ticket_type_id)

        if key == 'email':
            watcher.email = request.POST[key]
        
        if key == 'max_price':
            watcher.max_price = request.POST[key] or -1

        if key == 'num_tickets':
            watcher.num_tickets = request.POST[key] or -1

    watcher.uuid = str(uuid.uuid1())

    watcher.save()

    for ticket_type_id in ticket_types:
        watcher.types.add(TicketReductionType.objects.get(pk=ticket_type_id))

    watcher.save()

    redirect_url = reverse('concert', args=(concert_id,)) + f"?watcher_id={watcher.uuid}"
    return redirect(redirect_url)


### actions
def loadConcerts(request):
    num_concerts = actions.loadConcerts()

    # load tickets for 100 first future concerts
    first_100_future = Concert.objects.filter(datetime__gte = datetime.date(datetime.now())).order_by('datetime')[:100]
    for concert in first_100_future:
        actions.loadTickets(concert.id)

    return HttpResponse(f"Loaded {num_concerts} concerts")

def loadTickets(request, concert_id):
    num_tickets = actions.loadTickets(concert_id)
    return HttpResponse(f"Loaded {num_tickets} tickets")

def checkWatchers(request):
    actions.checkWatchers()
    return HttpResponse("Checked watchers")

def sendTestEmail(request):
    email = request.GET.get("email") or "nils.hellerhoff@gmail.com"
    actions.sendTestEmail(recipient=email)
    return HttpResponse("Sent test mail")

def deleteWatcher(request, uuid):
    watcher = get_object_or_404(Watcher, uuid=uuid)
    watcher.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
