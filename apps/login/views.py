from django.shortcuts import render, redirect, reverse
from .models import *
from django.contrib import messages

# Create your views here.
def landing(request):
    return render(request, 'login/landing.html')

def process(request):
    print 'entered process'
    if 'register' in request.POST:
        print 'register'
        errors = User.objects.validate_registration(request.POST)
        if 'error' in errors:
            for error in errors['error']:
                messages.add_message(request, messages.INFO, error)
            return redirect(reverse('login:landing'))
        if 'success' in errors:
            user = User.objects.register_user(request.POST)
            request.session['user_id']=user.id
            return redirect(reverse('dashboard:dashboard')) #this takes us to the dashboard app

    if 'login' in request.POST:
        print 'login'
        errors = User.objects.validate_login(request.POST)
        if 'error' in errors:
            for error in errors['error']:
                messages.add_message(request, messages.INFO, error)
            return redirect(reverse('login:landing'))

        if 'success' in errors:
            user_id = errors['success']
            request.session['user_id']=user_id
            return redirect(reverse('login:dashboard'))

    pass #might be good to return someone to hell in this case

def dashboard(request):
    if not 'user_id' in request.session:
        # in the future I could send someone to hell here
        return redirect(reverse('landing'))
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {
        'id':user_id,
        'first_name':user.first_name,
        'last_name':user.last_name,
        'email':user.email,
        'created_at':str(user.created_at)
    }
    return render(request, 'login/dashboard.html', context)

def logout(request):
    print 'entered logout'
    del request.session['user_id']
    return redirect(reverse('login:landing'))
