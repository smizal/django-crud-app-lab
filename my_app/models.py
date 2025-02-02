from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

ROOMS = (
    ('H1', 'Hall 1'),
    ('H2', 'Hall 2'),
    ('H3', 'Hall 3'),
    ('H4', 'Hall 4'),
    ('H5', 'Hall 5'),
    ('H6', 'Hall 6'),
)

# Create your models here.
class Feature(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    color = models.CharField(max_length=20)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feature-detail', kwargs={'pk': self.id})

class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    features = models.ManyToManyField(Feature)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} ON {self.date}"

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.id})

class Room(models.Model):
    date = models.DateField()
    room = models.CharField(
        max_length=2,
        choices=ROOMS,
        default=ROOMS[0][0]
    )
    event = models.ForeignKey(Event, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.event} : {self.get_room_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']