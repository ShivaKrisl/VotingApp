from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from .models import Electioncandidates
from django.contrib import messages
from django.utils import timezone
import bcrypt
# Create your views here.

def adminRegister(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass']
        user = User.objects.create_user(username=username)
        user.set_password(pass1)  # Set the password using set_password method
        user.save()
        messages.success(request,"Your account has successfully created")
        return render(request,'ecadmin')
    return render(request,'registration/adminRegister.html')

def ecadmin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password'] 
        try:
            # print(f"Attempting authentication with email ID: {username}")  
            user = authenticate(request, username=username, password=pass1)
            # print(f"user after authentication: {user}")  
            if user is not None:
                login(request, user)
                # print(f"user after authentication: {user}") 
                name = user.get_username()
                # print(name)
                # print(reverse('admindashboard'))
                return redirect(reverse('Candidates:admindashboard') + f'?name={name}&user_id={user.id}')
                # return redirect(reverse(request, 'admin_dashboard'))
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except Exception as e:
            print(e)
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'registration/admin.html')




def admindashboard(request):
    name = request.GET.get('name')
    user_id = request.GET.get('user_id') 
    if name and user_id:
        try:
            user = User.objects.get(id=user_id)
            return render(request, 'admin/index.html', {'user': user, 'name': name})
        except User.DoesNotExist:
            return  render(request,'registration/admin.html')
    else:
        return render(request,'registration/admin.html')

def addCandidates(request):
    name = request.GET.get('name')
    user_id = request.GET.get('user_id') 
    if name and user_id:
        try:
            user = User.objects.get(id=user_id)
            return render(request, 'admin/addCandidates.html', {'user': user, 'name': name})
        except User.DoesNotExist:
            return  render(request,'registration/admin.html')
    else:
        return render(request,'registration/admin.html')
    

def AddCandidate(request):
    name = request.POST.get('username')
    user_id = request.POST.get('user_id') 
    if name or user_id:
        try:
            if request.method == "POST":
            
                cid = request.POST['cid']
                cname = request.POST['cname']
                age = request.POST['age']
                education = request.POST['education']
                gender = request.POST['gender']
                partyname = request.POST['partyname']
                candimage = request.FILES['candimage']
                partyimage = request.FILES['partyimage']
                starttime = request.POST['starttime']
                endtime = request.POST['endtime']
                starttime = timezone.make_aware(timezone.datetime.strptime(starttime, '%Y-%m-%dT%H:%M'))
                endtime = timezone.make_aware(timezone.datetime.strptime(endtime, '%Y-%m-%dT%H:%M'))
                votecount = request.POST['votecount']
                # print("hi")
                # print(cid,cname,age,education,gender,partyname,starttime,endtime,votecount)
                user = Electioncandidates.objects.create(candidateID = cid,name = cname,age = age,gender = gender,education=education,photo=candimage,party_name = partyname,party_symbol = partyimage,start_time = starttime, end_time = endtime, votes=votecount)
                user.save()
                # print(user.objects.count())
                messages.success(request,"Candidate has Successfully added to the Election")
                return redirect(reverse('Candidates:addCandidates'))
            else:
                print("chudu")
                messages.error(request, "An error occurred")
                return redirect('Candidates:adminLogin')
        except Exception as t:
            print(t)
            messages.error(request, f"An error occurred: {t}")
            # return  render(request,'registration/admin.html')
    else:
        # print("here")
        return redirect(reverse('Candidates:admindashboard'))
def deleteCandidates(request):
    name = request.GET.get('name')
    user_id = request.GET.get('user_id') 
    print(name)
    print(user_id)
    if name and user_id:
        try:
            user = User.objects.get(id=user_id)
            return render(request, 'admin/deleteCandidate.html', {'user': user, 'name': name})
        except User.DoesNotExist:
            return  render(request,'registration/admin.html')
    else:
        return render(request,'registration/admin.html')
    

def fetch_candidate_details(request):
    if request.method == 'POST':
        # print(request.POST)
        candidateID = request.POST['candidateID']
        user_id = request.POST['user_id']
        name = request.POST['username']
        if user_id or name:
            try:
                user = User.objects.get(username = name)
                # print(candidateID)
                candidate = Electioncandidates.objects.get(candidateID=candidateID)
                # print(candidate)
                candidate_details = {
                        'candidateID': candidate.candidateID,
                        'name': candidate.name,
                        'age': candidate.age,
                        'gender': candidate.gender,
                        'education': candidate.education,
                        'image':candidate.photo,
                        'partyname':candidate.party_name,
                        'partysymbol': candidate.party_symbol,
                    }
                # print(candidate_details)
                return render(request, 'admin/deletionPage.html', {'user': user,'candidate':candidate})
            except Electioncandidates.DoesNotExist:
                print("here")
                return redirect('Candidates:adminLogin')
        else:
            return redirect('Candidates:adminLogin')
    else:
        return redirect('Candidates:adminLogin')
    
def deletion(request):
    if request.method == 'POST':
        name = request.POST['username']
        user_id = request.POST['user_id']
        # print(name,user_id)
        if name and user_id:
            try:
                candidateID = request.POST['candidate']
                cand = Electioncandidates.objects.get(candidateID = candidateID)
                print(cand)
                cand.delete()
                return redirect('Candidates:adminLogin')
            except Exception as e:
                messages.error(request,f"error unable to delete  =  {e}")
        else:
            messages.error(request,f"error Invalid Access  =  {e}")
            # return redirect('Candidates:adminLogin') 
    else:
        messages.error(request,f"error   =  {e}")
        # return redirect('Candidates:adminLogin') 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))