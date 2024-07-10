from django.contrib import admin
from django.urls import path,include
from . import views
from .admin import custom_admin_site
app_name = 'Candidates'

#  super user -> shivakrishna; shiva0508

urlpatterns = [
   path("",views.ecadmin,name="adminLogin"),
    path("adminRegister/",views.adminRegister,name="adminRegister"),
    path("admindashboard/",views.admindashboard,name="admindashboard"),
    path("addCandidates/",views.addCandidates,name="addCandidates"),
    path("AddCandidate/",views.AddCandidate,name="AddCandidate"),
    path("deleteCandidates/",views.deleteCandidates,name="deleteCandidates"),
    path('fetch-candidate-details/', views.fetch_candidate_details, name='fetch_candidate_details'),
    path('deletion/', views.deletion, name='deletion'),
]