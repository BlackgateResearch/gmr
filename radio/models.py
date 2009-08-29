from django.db import models   

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
    
    def getDeviation(self,Speed,Combat,Suspense,Positive):
        deviationSpeed = int(Speed) - self.gSpeed
        deviationCombat = int(Combat) - self.gCombat
        deviationSuspense = int(Suspense) - self.gSuspense
        deviationPositive = int(Positive) - self.gPositive
        
        deviation = deviationSpeed + deviationCombat + deviationSuspense + deviationPositive
        
        return deviation

#------------------------------
# demo data

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
