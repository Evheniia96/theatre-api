from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from theatre.models import (
    Genre,
    Actor,
    Play,
    Perfomance,
    TheatreHall,
    Ticket,
    Reservation,
)
from theatre.serializers import (
    GenreSerializer,
    ActorSerializer,
    PlaySerializer,
    PerfomanceSerializer,
    TheatreHallSerializer,
    TicketSerializer,
    ReservationSerializer,
)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class PerfomanceViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Perfomance.objects.all()
    serializer_class = PerfomanceSerializer


class TheatreHallViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class TicketViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
