from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse

from .constants import PROVIDERS
from .models import Concert, Ticket, TicketReductionType, Watcher

from . import actions

from datetime import datetime, timedelta

import json
import uuid
from django.core import serializers


def index(request):
    concerts = Concert.objects.filter(datetime__gte=datetime.date(datetime.now())).order_by('datetime')
    concerts_json = serializers.serialize("json", concerts)

    # adding ticket info (yes this is stupid)
    concerts2 = json.loads(concerts_json)
    for entry in concerts2:
        concert = Concert.objects.get(id=entry["pk"])
        entry["fields"]["available_tickets"] = concert.available_tickets

    context = {
        'concerts': concerts2,
        'providers': PROVIDERS
    }

    return render(request, 'ticketswatcher/index.html', context)


def watchers(request):
    email = request.GET.get("email")
    watchers = Watcher.objects.filter(email=email, concert__datetime__gte=datetime.date(datetime.now())).order_by(
        'concert__datetime')
    context = {
        'watchers': watchers,
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

    actions.load_tickets(concert_id)
    concert = get_object_or_404(Concert, pk=concert_id)

    tickets = Ticket.objects.filter(concert_id=concert_id).order_by('sort', '-price')
    ticket_reduction_types = Ticket.objects.filter(concert_id=concert_id).values('reduction_type__name',
                                                                                 'reduction_type__id').distinct()
    ticket_categories = Ticket.objects.filter(concert_id=concert_id).values('category').distinct()

    return render(request, 'ticketswatcher/concert.html', {
        'concert': concert,
        'concert_details': "\n".join([line.strip() for line in concert.details.split("\n")]),
        'provider': next(filter(lambda p: p['name'] == concert.provider, PROVIDERS))['title'],
        'tickets': tickets,
        'ticket_reduction_types': ticket_reduction_types,
        'ticket_categories': ticket_categories,
        'watcher_status': watcher_status,
        'watcher': watcher
    })


def watch(request, concert_id):
    concert = get_object_or_404(Concert, pk=concert_id)

    watcher = Watcher()

    watcher.concert = concert

    ticket_reduction_types = request.POST.get("ticket_reduction_types").split(", ")
    ticket_reduction_types = [int(t) for t in ticket_reduction_types if t.isnumeric()]

    watcher.email = request.POST.get("email")
    watcher.max_price = request.POST.get("max_price") or -1
    watcher.num_tickets = request.POST.get("num_tickets") or -1

    # for key in request.POST.keys():
    #     # if key.startswith('ticket_type_'):
    #     #     ticket_type_id = int(key.split('_')[2])
    #     #     ticket_types.append(ticket_type_id)
    #
    #     if key == 'email':
    #         watcher.email = request.POST[key]
    #
    #     if key == 'max_price':
    #         watcher.max_price = request.POST[key] or -1
    #
    #     if key == 'num_tickets':
    #         watcher.num_tickets = request.POST[key] or -1

    watcher.uuid = str(uuid.uuid1())

    watcher.save()

    for reduction_type_id in ticket_reduction_types:
        watcher.types.add(TicketReductionType.objects.get(pk=reduction_type_id))

    watcher.save()

    redirect_url = reverse('concert', args=(concert_id,)) + f"?watcher_id={watcher.uuid}"
    return redirect(redirect_url)


### actions
def loadConcerts(request):
    num_concerts = actions.loadConcerts()

    # load tickets for 100 first future concerts
    first_500_future = Concert.objects.filter(datetime__gte=datetime.date(datetime.now())).order_by('datetime')[:500]
    for concert in first_500_future:
        actions.load_tickets(concert.id)

    return HttpResponse(f"Loaded {num_concerts} concerts")


def loadTickets(request, concert_id):
    num_tickets = actions.load_tickets(concert_id)
    return HttpResponse(f"Loaded {num_tickets} tickets")


def checkWatchers(request):
    actions.check_watchers()
    return HttpResponse("Checked watchers")


def sendTestEmail(request):
    email = request.GET.get("email") or "nils.hellerhoff@gmail.com"
    actions.sendTestEmail(recipient=email)
    return HttpResponse("Sent test mail")


def deleteWatcher(request, uuid):
    watcher = get_object_or_404(Watcher, uuid=uuid)
    watcher.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
