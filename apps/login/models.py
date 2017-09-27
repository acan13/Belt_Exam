from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from datetime import datetime, date




# email regex for use later on
# edit, not actually used in this project
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self,form_data):
        # will append any errors with inputs to be shown after
        errors=[]


        # check name first
        if form_data['name'] == '':
            errors.append('Name is required.')
        else:
            if len(form_data['name'])<3:
                errors.append('Name must have at least 3 characters.')
            if not str.isalpha(str(form_data['name'].replace(' ',''))): #removes spaces when checking for non letters
                errors.append('Name may not contain numbers or symbols.')
                # add something to check if name is too long


        # now check username
        if form_data['username'] == '':
            errors.append('Username is required.')
        else:
            if len(form_data['username'])<3:
                errors.append('Username must have at least 3 characters.')
        if len(self.filter(username=form_data['username']))>0:
            errors.append('This username is already associated with an account.')

        # finally check password
        if not 'password' in form_data:
            errors.append('Password is required')
        else:
            if len(form_data['password'])<8:
                errors.append('Password must be at least 8 characters.')
            if form_data['password'] != form_data['pw_confirm']:
                errors.append('Passwords must match.')

        # if there are errors, will return the errors to be displayed
        if len(errors)>0:
            return {'error':errors}
        return {'success':'Successful registration attempt'}

    def validate_login(self,form_data):
        errors = []


        # check username
        if len(self.filter(username=form_data['username']))<1:
            errors.append('No account registered with this username.')
        else:
            user = self.filter(username=form_data['username'])[0]

            # check to see if password is valid iff username is ok
            if form_data['password'] == '':
                errors.append('Please enter your password.')
            elif not bcrypt.checkpw(str(form_data['password']),str(user.password)):
                errors.append('Incorrect password.')

        if len(errors)>0:
            return {'error':errors}
        return {'success':user.id}



    def register_user(self, form_data):
        user = User.objects.create()
        user.name = form_data['name']
        user.username = form_data['username']
        user.password = bcrypt.hashpw(str(form_data['password']),bcrypt.gensalt())
        user.save()

        return User.objects.last()



class User(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return str(self.username)





"""Trip tables and manager below"""










class TripManager(models.Manager):
    def validate_trip(self,form_data):
        # will append any errors with inputs to be shown after
        errors=[]


        # check destination first
        if form_data['destination'] == '':
            errors.append('Destination is required.')
        else:
            if len(form_data['destination'])<2:
                errors.append('Destination must have at least 2 characters.')
            # if not str.isalpha(str(form_data['destination'])):
            #     errors.append('Destination may not contain numbers or symbols.') #probably not needed for this


        # now check description
        if form_data['description'] == '':
            errors.append('Description is required.')
        else:
            if len(form_data['description'])<2:
                errors.append('Description must have at least 2 characters.')


        # check date_from
        if form_data['date_from'] == 'invalid':
            errors.append('Please enter a start date.')
        elif form_data['date_from'] < date.today():
            errors.append('Please enter a start date in the future.')


        # check date_to
        if form_data['date_to'] == 'invalid':
            errors.append('Please enter an end date.')
        else:
            if form_data['date_to'] < date.today():
                errors.append('Please enter an end date in the future.')
            if form_data['date_to'] < form_data['date_from']:
                errors.append('Please enter an end date that is after your start date.')


        # if there are errors, will return the errors to be displayed
        if len(errors)>0:
            return {'error':errors}
        return {'success':'Successful trip attempt'}


    def register_trip(self, form_data, user_id):
        # create trip
        # add user/creator to trip as organizer AND member
        user = User.objects.get(id=user_id)
        trip = Trip.objects.create(
            destination = form_data['destination'],
            description = form_data['description'],
            date_from = form_data['date_from'],
            date_to = form_data['date_to'],
            organizer = user
            )
        trip.save()
        trip.users.add(user)


        return Trip.objects.last().id

    def add_user(self,trip_id,user_id):
        # adds a user as a part of the trip, but not the organizer
        trip = Trip.objects.get(id=trip_id)
        user = User.objects.get(id=user_id)
        trip.users.add(user)

        return trip.id





class Trip(models.Model):
    destination=models.CharField(max_length=50)
    description=models.CharField(max_length=255)
    date_from=models.DateTimeField()
    date_to=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='joined_trips')
    organizer = models.ForeignKey(User,related_name='organized_trips')

    objects = TripManager()

    def __repr__(self):
        return str(self.destination)
