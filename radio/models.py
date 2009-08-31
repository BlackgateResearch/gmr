from django.db import models
from django import forms
from django.contrib.auth.models import User

class Track(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    art = models.CharField(max_length=200)
    #Genre params
    gSpeed = models.IntegerField()
    gCombat = models.IntegerField()
    gSuspense = models.IntegerField()
    gPositive = models.IntegerField()

    def __unicode__(self):
        return self.name
        
    def getGenre(self):
        return str(self.gSpeed) + str(self.gCombat) + str(self.gSuspense) + str(self.gPositive)
    
    def ensurePositive(self,val):
        if val < 0:
            return val * -1
        else:
            return val
    
    def getDeviation(self,Speed,Combat,Suspense,Positive):
        deviationSpeed = int(Speed) - self.gSpeed
        deviationCombat = int(Combat) - self.gCombat
        deviationSuspense = int(Suspense) - self.gSuspense
        deviationPositive = int(Positive) - self.gPositive
        
        deviation = self.ensurePositive(deviationSpeed) + self.ensurePositive(deviationCombat) + self.ensurePositive(deviationSuspense) + self.ensurePositive(deviationPositive)
        
        return deviation
        
class Feedback(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=100)
    subject = models.CharField(max_length=20)
    description = models.TextField()
    
    def __unicode__(self):
        return self.subject    

class GenreForm(forms.Form):
    speed = forms.CharField(max_length=1)
    combat = forms.CharField(max_length=1)
    suspense = forms.CharField(max_length=1)
    positive = forms.CharField(max_length=1)

# demo data

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
