from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^process$', views.process, name='login_process'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/logout$', views.logout, name='logout'),
]
