from django.db import models
from django.db import connection

class Concert(models.Model):
    provider = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=2000, null=True)
    datestr = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    ticketID = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200, null=True)
    ticket_url = models.CharField(max_length=200, null=True)
    venue = models.CharField(max_length=200, null=True)
    last_updated = models.DateTimeField(null=True)
    last_ticket_updated = models.DateTimeField(null=True)

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

    @property
    def available_tickets(self) -> int:
        query = f"""
SELECT
    sum(available) as available
FROM (
    SELECT
        max(available) as available
    FROM ticketswatcher_ticket
    WHERE concert_id = {self.id}
    GROUP BY category
)"""

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return row[0]


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
    types = models.ManyToManyField(TicketReductionType, blank=True)
    uuid = models.CharField(max_length=200, null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.concert.title}"

    def show_price(self):
        return self.max_price if self.max_price > 0 else '--'

    def show_num(self):
        return self.num_tickets if self.num_tickets > 0 else '--'

    def show_types(self):
        return ", ".join([ticket_type.name for ticket_type in self.types.all()])