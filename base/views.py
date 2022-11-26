from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# Queries to DB, template to render etc

# rooms = [
#     {"id": 1, "name": "Let's learn Python !"},
#     {"id": 2, "name": "Let's learn C++ !"},
#     {"id": 3, "name": "Let's learn Java !"},
# ]

def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
            
    context = {'page': page}
    
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    
    logout(request)
    
    return redirect('home')

def registerPage(request):

    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False) # Do not save yet. Let's clean it first
            user.username = user.username.lower()
            
            user.save()

            login(request, user)
            
            return redirect('home')
        else:
            messages.error = (request, 'An error occurred during registration!')
    
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

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
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
            
    context = {'room': room, 'room_messages' : room_messages, 'participants': participants }
    return render(request, 'base/room.html', context)

@login_required(login_url = 'login')
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

@login_required(login_url = 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allow to modify this item")
    
    # Take care of the input from user
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        
        # print(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home page
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allow to delete this item")
    
    # Take care of the input from user
    if request.method == 'POST':
        room.delete()
        return redirect('home')  # Redirect to home page
    
    # context = {'form': form}
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url = 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id = pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allow to delete this item")
    
    # Take care of the input from user
    if request.method == 'POST':
        message.delete()
        return redirect('home')  # Redirect to home page
    
    # context = {'form': form}
    
    return render(request, 'base/delete.html', {'obj': message})