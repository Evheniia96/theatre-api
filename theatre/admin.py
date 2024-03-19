from django.contrib import admin

from theatre.models import (Actor,
                            Genre,
                            TheatreHall,
                            Play,
                            Perfomance,
                            Reservation,
                            Ticket)

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(TheatreHall)
admin.site.register(Play)
admin.site.register(Perfomance)
admin.site.register(Reservation)
admin.site.register(Ticket)
