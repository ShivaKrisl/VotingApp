from django.contrib import admin
from django.urls import path,include
from validation import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("login/",views.loginUser,name="login"),
    path("Register/",views.registerDetails,name = "Register"),
    
    path("home/", views.home,name="home"),
    path("elections_overview/",views.elections_overview,name="elections_overview"),
    path('elections_guidelines/', views.elections_guidelines, name='elections_guidelines'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("candidatedetails/",views.candidatedetails,name="candidatedetails"),
    path("PollingBooth/",views.PollingBooth,name="PollingBooth"),
    path("countingElections/",views.countingElections,name="countingElections"),
    path("ResultsPage/",views.ResultsPage,name="ResultsPage"),
]
