from django.db import models

class Concert(models.Model):
    provider = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    datestr = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    ticketID = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200, null=True)
    ticket_url = models.CharField(max_length=200, null=True)
    venue = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.datetime} - {self.title}"

    @property
    def providerHR(self):
        providers = {
            'brticket': 'BR Ticket',
            'mphil': 'Münchner Philharmoniker',
            "brso": "BRSO",
        }
        return providers[self.provider]

class Ticket(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    price = models.IntegerField()
    category = models.CharField(max_length=200, null=True)
    sort = models.IntegerField()
    name = models.CharField(max_length=200, null=True)
    identifier = models.CharField(max_length=200, null=True)
    color = models.CharField(max_length=200, null=True)
    available = models.IntegerField()
    reduction_type = models.ForeignKey('TicketReductionType', on_delete=models.CASCADE, null=False)

class TicketReductionType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Watcher(models.Model):
    email = models.EmailField()
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    max_price = models.IntegerField()
    num_tickets = models.IntegerField()
    types = models.ManyToManyField(TicketReductionType)