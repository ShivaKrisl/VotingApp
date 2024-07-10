from django.contrib.auth.models import User
from django.db import models

from Candidates.models import Electioncandidates

class UserProfile(models.Model):
    username = models.CharField(max_length = 100,blank = False, null = False)
    email = models.EmailField(blank = False,null = False,unique = True)
    pass1 = models.CharField(max_length = 100,blank = False,null = False)
    voter_id = models.CharField(max_length=100, blank=False, null=False,unique = True)
    has_voted = models.BooleanField(default=False)

    def vote(self, candidate_id):
        if not self.has_voted:
            candidate = Electioncandidates.objects.get(candidateID=candidate_id)
            candidate.votes += 1
            candidate.save()
            self.has_voted = True
            self.save()
            return True
        else:
            return False
    
