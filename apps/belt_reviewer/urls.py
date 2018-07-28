from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^books$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^books/add$', views.add),
    url(r'^books/create$', views.create),
    url(r'^books/(?P<book_id>\d+)$', views.show),
    url(r'^books/create/(?P<book_id>\d+)$', views.review_create),
    url(r'^logout$', views.logout)
]
