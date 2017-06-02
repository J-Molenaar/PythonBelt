from django.shortcuts import render, redirect
from .models import Destination
from ..login.models import User
from django.contrib import messages
from django.db.models import Count
from django.core.urlresolvers import reverse
import datetime


def index(request):
    if "id" not in request.session:
        return redirect("login:index")
    context = {
        'user_trips': Destination.objects.filter(user_id=User.objects.get(id=request.session['id'])),
        'user': User.objects.get(id=request.session['id']),
        'other_trips':  Destination.objects.exclude(user_id=User.objects.get(id=request.session['id'])),
        }
    return render(request, 'main/index.html', context) #loads dashboard page

def add(request):
    print("$"*20)
    if "id" not in request.session:
        return redirect("login:index")
    return render(request, 'main/add.html') #loads add page

def add_trip(request):
    print("%"*20)
    user = User.objects.get(id=request.session['id'])
    trip = Destination.objects.add(request.POST, user)

    if trip[0] == False:
        print trip
        return redirect('main:index')
    else:
        errors = trip[1]
        for error in errors:
            messages.error(request, error)
        print messages
        return redirect('main:add')

def details(request, id):
    if "id" not in request.session:
        return redirect("login:index")
    return render(request, 'main/details.html') #loads details page

def join(request, id):
    add_data = {
    'trip_id': id,
    'user_id': request.session['id']
    }
    Destination.objects.add_user(add_data)
    return redirect('main:index', )

def details(request, id):
    if 'id' not in request.session:
        return redirect("login:index")

    context = {
    'trip': id,
    'users': User.objects.filter(join=id)
    }
    return render(request, 'main/details.html', context)
