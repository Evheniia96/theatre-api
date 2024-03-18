from django.conf import settings
from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Genre(models.Model):
    name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name


class TheatreHall(models.Model):
    name = models.CharField(max_length=55)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return (f"TheatreHall: {self.name},"
                f" rows: {self.rows} "
                f"(seats_in_row: {self.seats_in_row})")


class Play(models.Model):
    title = models.CharField(max_length=55)
    description = models.TextField()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Perfomance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE
    )
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return (f"Perfomance: {self.play.title},"
                f" show time: {self.show_time}")


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation: {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    perfomance = models.ForeignKey(Perfomance,
                                   on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return (f"Perfomance: {self.perfomance.play}."
                f"Ticket: {self.row} row,{self.seat} seat")

    class Meta:
        ordering = ["row", "seat"]
