from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^accounts/profile', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^apikey$', views.ApiKeyGenerator, name='genapi'),
    url(r'^chckapi$', views.AccessTokenGenerator, name='apicheck'),
    url(r'^csvdwnld$', views.File_Download, name='dwnldcsv'),
    url(r'openapi$',views.OpenApiPage,name='openapi'),
    url(r'^dashboard$', views.openDashboard, name='dashboard'),
    url(r'^pay$', views.openPaymentPage, name='pay'),
    url(r'^home$', views.openHomePage, name='home'),
    url(r'^successfulPayment$', views.getSuccessfulTransactionData, name='successfulPayment'),
    url(r'^PlanActivate$',views.free_pln, name = 'freepln'),
]
