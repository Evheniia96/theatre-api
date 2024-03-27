from django.contrib import admin

from theatre.models import (
    Actor,
    Genre,
    TheatreHall,
    Play,
    Performance,
    Reservation,
    Ticket,
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(TheatreHall)
admin.site.register(Play)
admin.site.register(Performance)
admin.site.register(Ticket)
