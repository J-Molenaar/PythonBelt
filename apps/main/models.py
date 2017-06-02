from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
from ..login.models import User
from datetime import date

# Create your models here.

class DestinationManager(models.Manager):
    def add(self, postData, user):
        errors = []
        if len(postData['destination']) < 1:
            errors.append("Destination cannot be blank.")
        if len(postData['description']) < 1:
            errors.append("Description cannot be blank.")
        if len(postData['start']) < 1:
            errors.append("Start date cannot be blank.")
        if len(postData['end'])< 1:
            errors.append("End date cannot be blank.")
        if postData["start"] < str(date.today()):
			errors.append("That date is a past date. Please select a furture date.")
        if postData['start'] > postData['end']:
            errors.append("You cannot end before you start.")

        if errors:
            return(True, errors)
        else:
            trip=Destination.objects.create(destination=postData["destination"], description=postData["description"], start=postData["start"], end=postData["end"], creator=user)
            trip.user_id.add(user)
            trip.save()
            return (False, trip)

    def add_user(self, data):
        trip = Destination.objects.get(id = data['trip_id'])
        user = User.objects.get(id=data['user_id'])
        trip.user_id.add(user)
        return

class Destination(models.Model):
    destination = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    description = models.TextField()
    creator = models.ForeignKey(User, related_name="creator")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ManyToManyField(User, related_name='join')
    objects = DestinationManager()
