from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# Queries to DB, template to render etc

# rooms = [
#     {"id": 1, "name": "Let's learn Python !"},
#     {"id": 2, "name": "Let's learn C++ !"},
#     {"id": 3, "name": "Let's learn Java !"},
# ]

def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does not exist!')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login Failed. Username or Password is incorrect !')
            
    context = {}
    
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    
    logout(request)
    
    return redirect('home')

def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) |
        Q(description__icontains = q) 
    )
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count }
    
    return render(request, 'base/home.html', context)

def room(request, pk):
    # room = None
    
    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i
    
    room = Room.objects.get(id=pk)
    
            
    context = {'room': room }
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    
    # Take care of the input from user
    if request.method == 'POST':
        form = RoomForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home page
        else:
            raise Http404
    
    context = {'form': form}
    
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # Take care of the input from user
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        
        # print(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home page
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    
    # Take care of the input from user
    if request.method == 'POST':
        room.delete()
        return redirect('home')  # Redirect to home page
    
    # context = {'form': form}
    
    return render(request, 'base/delete.html', {'obj': room})

