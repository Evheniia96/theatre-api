from rest_framework import serializers
from theatre.models import (Actor,
                            Genre,
                            TheatreHall,
                            Play,
                            Perfomance,
                            Reservation,
                            Ticket)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description")


class PerfomanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfomance
        fields = ("id", "play", "theatre_hall", "show_time")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "perfomance", "reservation")
