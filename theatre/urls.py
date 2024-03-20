from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    PerfomanceViewSet,
    TheatreHallViewSet,
    TicketViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("plays", PlayViewSet)
router.register("perfomances", PerfomanceViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("tickets", TicketViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]


app_name = "theatre"
