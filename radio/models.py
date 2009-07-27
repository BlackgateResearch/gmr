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
    
    def getDeviation(self,gSpeed,gCombat,gSuspense,gPositive):
        deviation = 1 # replace this with deviation calculating code
        return devation

#------------------------------
# demo data

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice = models.CharField(max_length=200)
#    votes = models.IntegerField()

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
