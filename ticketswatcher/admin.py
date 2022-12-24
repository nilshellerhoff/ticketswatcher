from django.contrib import admin

from .models import Concert, Ticket, Watcher

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 3
    fieldsets = [
        (None, {'fields': ['reduction_type', 'price']}),
    ]

class ConcertAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    search_fields = ['title']

admin.site.register(Concert, ConcertAdmin)
admin.site.register(Watcher)