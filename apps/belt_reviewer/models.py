# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import bcrypt
from django.core.validators import MinValueValidator

# Create your models here.
class UserManager(models.Manager):
    def validate(self, request):
        if request.method == 'POST':
            valid = True
            for x in request.POST:
                if request.POST[x] == '':
                    valid = False
                    messages.error(request, '{} is required'.format(x))
            if request.POST['password'] != request.POST['confirm_pass']:
                valid = False
                messages.error(request, 'Passwords do not match, try again.')
            if valid:
                crypto_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

                self.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=crypto_pass)
                messages.success(request, 'Successfully registered.')

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {}>".format(self.first_name, self.last_name)

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "<Author object: {}>".format(self.name)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews')
    content = models.TextField(max_length=255)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)