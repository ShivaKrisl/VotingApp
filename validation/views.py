from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile 
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from Candidates.models import Electioncandidates
from django.http import JsonResponse

# Create your views here.
def loginUser(request):
    if request.method == "POST":
        voterid = request.POST['voterid']
        pass1 = request.POST['password']
        try:
            user = UserProfile.objects.get(voter_id=voterid,pass1 = pass1)  # Get the user object
            if user is not None:
                # print(user)
                # user = authenticate(request, username=user.username, password=pass1)
                # login(request, user)  # Authenticate using the retrieved user
                name = user.username
                return redirect(reverse('home') + f'?name={name}&user_id={user.id}')

            else:  # This shouldn't happen if user object was retrieved
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('login')

        except UserProfile.DoesNotExist:  # Handle case where UserProfile doesn't exist
            messages.error(request, "Invalid Voter ID.")
            return redirect('login')

    return render(request, "registration/login.html")


def registerDetails(request):
    if request.method == "POST":
          username = request.POST['username']
          mail = request.POST['mailid']
          voterid = request.POST['voterid']
          pass1 = request.POST['password']
          user = UserProfile.objects.create(username = username,email = mail,voter_id = voterid, pass1 = pass1)
          user.save()
          messages.success(request,"Your account has successfully created")

          return redirect('login')
    return render(request,'registration/Register.html')


def home(request):
        
    name = request.GET.get('name')
    user_id = request.GET.get('user_id') 
    if name and user_id:
        try:
            user = UserProfile.objects.get(id=user_id)
            print(user.id)
            return render(request, 'home.html', {'user': user, 'name': name})
        except User.DoesNotExist:
            return  render(request,'registration/login.html')
    else:
        return render(request,'registration/login.html')
    
# @login_required
def elections_overview(request):
    user_id = request.GET.get('user_id')
    name = request.GET.get('name')
    # return render(request, 'elections_overview.html')
    if name and user_id:
        try:
            # user = User.objects.get(id=user_id)
            user = UserProfile.objects.get(id=user_id)
            return render(request, 'elections_overview.html',{"user":user,"name":name})
        except User.DoesNotExist:
            return  render(request,'registration/login.html')
    else:
        return render(request,'registration/login.html')
    
def elections_guidelines(request):
    user_id = request.GET.get('user_id')
    name = request.GET.get('name')
    # return render(request, 'elections_overview.html')
    if name and user_id:
        try:
            user = UserProfile.objects.get(id=user_id)
            return render(request, 'elections_guidelines.html',{"user":user,"name":name})
        except User.DoesNotExist:
            return  render(request,'registration/login.html')
    else:
        return render(request,'registration/login.html')
    
def candidatedetails(request):
    user_id = request.GET.get('user_id')
    name = request.GET.get('name')
    # return render(request, 'elections_overview.html')
    if name and user_id:
        try:
            user = UserProfile.objects.get(id=user_id)
            current_time = timezone.now()
            candidates = Electioncandidates.objects.all()
            # print(candidates)
            return render(request, 'candidateDetails.html',{"name":name,"user":user,"current_time":current_time, "candidates" : candidates})
        except User.DoesNotExist:
            return  render(request,'registration/login.html')
    else:
        return render(request,'registration/login.html')
    

    
def PollingBooth(request):
    user_id = request.GET.get('user_id')
    name = request.GET.get('name')
    if name and user_id:
        try:
            user = UserProfile.objects.get(id = user_id)
            # print(user)
            current_time = timezone.now()
            candidates = Electioncandidates.objects.all()
            # print(candidates)
            return render(request, 'ElectionsLive.html',{"name":name,"current_time":current_time, "candidates" : candidates,"user":user})
        except User.DoesNotExist:
            return  render(request,'registration/login.html')
    else:
        return render(request,'registration/login.html')
    

# from django.utils import timezone
# from .models import Electioncandidates

def countingElections(request):
    if request.method == 'POST':
        try:
            # user_id = request.POST['user_id']
            name = request.POST['name']
            user_id = request.POST['user_id']
            candidate_id = request.POST['candidate_id']
            current_time = timezone.now()
            # print(name,candidate_id,user_id)
            # Check if user_id and name are provided
            if name and user_id:
                # Query the candidate by candidate_id
                # print(User.objects.all())
                user = UserProfile.objects.get(id = user_id)
                # print(UserProfile.objects.all())
                # print(user)
                candidate = Electioncandidates.objects.get(candidateID=candidate_id)
                print(candidate.start_time,candidate.end_time,current_time,user.has_voted)
                if candidate.start_time <= current_time and candidate.end_time > current_time and user.has_voted == False:
                    print("here")
                    candidate.votes += 1
                    user.has_voted = True
                    user.save()
                    candidate.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'Election is not active.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid user data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def ResultsPage(request):
    user_id = request.GET.get('user_id')
    name = request.GET.get('name')
    if user_id and name:
        try :
            user = UserProfile.objects.get(id = user_id)
            if user:
                # print(user)
                candidates = Electioncandidates.objects.all()
                if candidates:
                    current_time = timezone.now()
                    maxi = 0
                    winner = candidates[0]
                    # print(winner)
                    for c in candidates:
                        if c.votes > maxi:
                            maxi = c.votes
                            winner = c
                    # print(winner.candidateID)
                    return render(request, 'ResultsPage.html',{"user":user,"name":name,"candidates":candidates,"current_time":current_time, "winner":winner})
        except Exception as e:
            print(e)
            return redirect('login')
    # print("j")
    return redirect('login')
        
    