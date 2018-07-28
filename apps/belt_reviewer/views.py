# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django import forms
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from .models import User, Author, Book, Review
import bcrypt
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
LOGIN_REGEX = r"(^[a-zA-Z]+$)"



# Create your views here.
def index(request):

    if 'id' in request.session:
        return redirect('/dashboard')

    # if request.session['id'] :
    #     return redirect('/books')

    return render(request, 'belt_reviewer/index.html')


def register(request):
    User.objects.validate(request)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        valid = True
        email = request.POST['email']
        password = request.POST['password']

        get_user = User.objects.filter(email = email)

        if len(get_user) > 0:
            user = get_user[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()) == True:
                request.session['id'] = user.id
                request.session['name'] = user.first_name
                return redirect('/dashboard')

        messages.error(request, "Invalid login information")
        return redirect('/')

    return redirect('/')


    #     if not get_user:
    #         valid = False
    #         print(get_user)
    #         messages.add_message(request, messages.ERROR, 'Email not found, please try again')
    #         return redirect('/')
    #
    #     check_pass = User.objects.get(email = email)
    #
    #     if not bcrypt.checkpw(password.encode(), check_pass.password.encode()):
    #         valid = False
    #         messages.add_message(request, messages.ERROR, 'Email/Password is incorrect, please try again.')
    #         return redirect('/')
    #
    #     if not valid:
    #         if 'id' not in request.session:
    #             return redirect('/')
    #         else:
    #             return redirect('/books')
    #     else:
    #         request.session['id'] = check_pass.id
    #         request.session['name'] = check_pass.first_name
    #         messages.add_message(request, messages.SUCCESS, 'You have successfully logged in.')
    #         return render(request, 'belt_reviewer/dashboard.html', {"user": check_pass})
    #
    # if 'id' in request.session:
    #     return redirect('/dashboard')

    # return redirect('/')


def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')

    reviews = Review.objects.all().order_by("-created_at")[0:3]

    ids = []
    for review in reviews:
        ids.append(review.book.id)

    context = {
        "latest_three": reviews,
        "other_books": Book.objects.exclude(id__in=ids)
    }

    return render(request, 'belt_reviewer/dashboard.html', context)


def add(request):
    if 'id' not in request.session:
        return redirect('/')

    context = {
        "authors": Author.objects.all()
    }
    return render(request, 'belt_reviewer/review.html', context)


def create(request):
    if request.method == 'POST':
        valid = True

        book_title = request.POST['title']
        review = request.POST['review']
        rating = request.POST['rating']
        author_name = request.POST['input_author']

        if author_name == '':
            author_name = request.POST['select_author']

        author = Author.objects.filter(name = author_name)

        if len(author) == 0:
            author = Author.objects.create(name = author_name)
        else:
            author = author[0]

        book = Book.objects.filter(title=book_title)

        if len(book) == 0:
            book = Book.objects.create(title = book_title, author=author)
        else:
            book = book[0]

        user = User.objects.get(id = request.session['id'])

        Review.objects.create(content = review, rating = rating, user=user, book=book)

        return redirect('/books/' + str(book.id))

        # if book_title == '':
        #     valid = False
        #     messages.add_message(request, messages.ERROR, 'Title cannot be blank.')
        #     return redirect('/books/add')
        #
        # if review == '':
        #     valid = False
        #     messages.add_message(request, messages.ERROR, 'Review cannot be blank.')
        #     return redirect('/books/add')
        #
        # if rating == '':
        #     valid = False
        #     messages.add_message(request, messages.ERROR, 'Review cannot be blank.')
        #     return redirect('/books/add')

        # if not valid:
        #     return redirect('/books/add')
        # else:
        #     return redirect('/books/add')


def show(request, book_id):
    context = {
        "book": Book.objects.get(id=book_id)
    }
    return render(request, 'belt_reviewer/showbook.html', context)


def review_create(request, book_id):
    review = request.POST['review']
    rating = request.POST['rating']

    book = Book.objects.get(id=book_id)

    user = User.objects.get(id=request.session['id'])

    Review.objects.create(content=review, rating=rating, user=user, book=book)

    return redirect('/books/' + str(book.id))


def logout(request):
    request.session.clear()
    return redirect('/')



