from django.shortcuts import render, redirect, reverse
from ..login.models import *
from django.contrib import messages
from time import strftime, strptime, mktime
from datetime import datetime

# Create your views here.
def index(request):
    if not 'login_id' in request.session:
        return redirect(reverse('login:landing'))

    # move these to models when you get a chance

    # add proper context
    # start with user info
    user = User.objects.get(id=request.session['login_id'])
    context={}
    context['user']={'name':user.name,'trips':[]}
    print 'context after user',context

    # now add user's trips
    trips = user.joined_trips.all()
    context['user']['trips']=[]
    for trip in trips:
        context['user']['trips'].append({
            'id':trip.id,
            'destination':trip.destination,
            'organizer':trip.organizer.name,
            'description':trip.description,
            'date_from':trip.date_from.strftime("%b %d, %Y"),
            'date_to':trip.date_to.strftime("%b %d, %Y")
        })
    print 'context after user trips',context

    # now add other users' trips
    trips = Trip.objects.all().exclude(organizer=user).exclude(users=user)
    print trips
    context['others']={'trips':[]}
    for trip in trips:
        context['others']['trips'].append({
            'destination':trip.destination,
            'date_from':trip.date_from.strftime("%b %d, %Y"),
            'date_to':trip.date_to.strftime("%b %d, %Y"),
            'id':trip.id,
            'user':{'name':trip.organizer.name}
        })

    return render(request, 'dashboard/dashboard.html', context)








def destination(request, trip_id):
    if not 'login_id' in request.session:
        return redirect(reverse('login:landing'))

    # prepares trip data for display
    trip = Trip.objects.get(id=trip_id)
    context={}
    context['trip']={
        'destination':trip.destination,
        'description':trip.description,
        'date_from':trip.date_from.strftime("%b %d, %Y"),
        'date_to':trip.date_to.strftime("%b %d, %Y"),
        'organizer':{'name':trip.organizer.name}
    }

    # prepares data to display other users participating
    # in the trip. Excludes organizer from this list.
    organizer_id = trip.organizer.id
    users = trip.users.all().exclude(id=organizer_id)
    context['trip']['users']=[]
    for user in users:
        context['trip']['users'].append({'name':user.name})
        print user.name

    return render(request, 'dashboard/show_trip.html', context)








def join_trip(request, trip_id):
    if not 'login_id' in request.session:
        return redirect(reverse('login:landing'))

    Trip.objects.add_user(trip_id,request.session['login_id'])
    messages.add_message(request, messages.INFO, 'You have successfully joined this trip!')
    # in the future add a message saying it was successful

    # once added, sends them to the trip page
    return redirect(reverse('dashboard:destination', kwargs={'trip_id':trip_id}))
    pass







def add_travel(request):
    if not 'login_id' in request.session:
        return redirect(reverse('login:landing'))

    return render(request, 'dashboard/add_trip.html')






def process_add_travel(request):
    if not 'login_id' in request.session:
        return redirect(reverse('login:landing'))


    # I'm sure there's a better way than this
    # but I looked really hard and ran out of time
    # before finding it
    form_data = {}
    try:
        form_data['date_from']=datetime.fromtimestamp(mktime(strptime(str(request.POST['date_from']),'%Y-%m-%d'))).date()
    except:
        form_data['date_from']='invalid'
    try:
        form_data['date_to']=datetime.fromtimestamp(mktime(strptime(str(request.POST['date_to']),'%Y-%m-%d'))).date()
    except:
        form_data['date_to']='invalid'
    form_data['destination']=request.POST['destination']
    form_data['description']=request.POST['description']

    # check for valid input
    errors = Trip.objects.validate_trip(form_data)
    print 'errors',errors
    if 'error' in errors:
        for error in errors['error']:
            messages.add_message(request, messages.INFO, error)
        return redirect(reverse('dashboard:add_travel'))
    """
    trip_id = Trip.objects.register_trip(request.POST,request.session['login_id'])
    """
    return redirect(reverse('dashboard:add_travel')) #temporary
    return redirect(reverse('dashboard:destination',kwargs={'trip_id':trip_id}))
