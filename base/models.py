from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Define database
# run python manage.py makemigrations to create this model

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True) # auto_now add timestamp every time we update
    created = models.DateTimeField(auto_now_add=True) # auto_now_add only add first time we created it
    
    class Meta:
            ordering = ['-updated', '-created']  # Order by updated in reverse order and then order by created 
    
    def __str__(self) -> str:
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # auto_now add timestamp every time we update
    created = models.DateTimeField(auto_now_add=True) # auto_now_add only add first time we created it
    
    def __str__(self) -> str:
        return self.body[0:50]     # Return first 50 characters
