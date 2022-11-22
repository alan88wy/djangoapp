from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# Create your views here.
# Queries to DB, template to render etc

# rooms = [
#     {"id": 1, "name": "Let's learn Python !"},
#     {"id": 2, "name": "Let's learn C++ !"},
#     {"id": 3, "name": "Let's learn Java !"},
# ]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    
    return render(request, 'base/home.html', context)

def room(request, pk):
    # room = None
    
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i
    
    room = Room.objects.get(id=pk)
            
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    
    context = {'form': form}
    
    return render(request, 'base/room_form.html', context)

