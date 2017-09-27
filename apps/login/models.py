from __future__ import unicode_literals
import re, bcrypt
from django.db import models


# email regex for use later on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self,form_data):
        # will append any errors with inputs to be shown after
        errors=[]

        # changes email to lower case before running any checks on it
        # this avoids accidental duplicates
        email=form_data['email'].lower()

        # check first name first
        if form_data['first_name'] == '':
            errors.append('First name is required.')
        else:
            if len(form_data['first_name'])<2:
                errors.append('First name must have at least 2 characters.')
            if not str.isalpha(str(form_data['first_name'])):
                errors.append('First name may not contain numbers or symbols.')

        # now check last name
        if form_data['last_name'] == '':
            errors.append('Last name is required.')
        else:
            if len(form_data['last_name'])<2:
                errors.append('Last name must have at least 2 characters.')
            if not str.isalpha(str(form_data['last_name'])):
                errors.append('Last name may not contain numbers or symbols.')

        # now check email
        if email == '':
            errors.append('Email is required.')
        elif not EMAIL_REGEX.match(email):
            errors.append('Please enter a valid email.')
        if len(self.filter(email=email))>0:
            errors.append('This email address is already associated with an account.')

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

        # changes email to lower case before running any checks on it
        email=form_data['email'].lower()

        # check email
        if not EMAIL_REGEX.match(email):
            errors.append('Please enter a valid email address.')
        elif len(self.filter(email=email))<1:
            errors.append('No account registered with this email address.')
        else:
            user = self.filter(email=email)[0]

            # check to see if password is valid iff email is ok
            if form_data['password'] == '':
                errors.append('Please enter your password.')
            elif not bcrypt.checkpw(str(form_data['password']),str(user.password)):
                errors.append('Incorrect password.')

        if len(errors)>0:
            return {'error':errors}
        return {'success':user.id}



    def register_user(self, form_data):
        user = User.objects.create()
        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']
        user.email = email.lower()
        user.password = bcrypt.hashpw(str(form_data['password']),bcrypt.gensalt())
        user.save()

        return User.objects.last()



class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return str(self.first_name)+' '+str(self.last_name)
