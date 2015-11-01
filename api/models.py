from django.db import models

#Here we create the models for players' data

class PuzzleData(models.Model):
    puzzles = models.IntegerField()
    scores = models.IntegerField()
    stars = models.IntegerField()

    def __str__(self):
        return "Level: "+str(self.level)+" Score:"+str(self.score) +" Stars:"+str(self.stars)

class Player(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=60)
    social_id = models.CharField(max_length=120)
    puzzle_data = models.ManyToManyField(PuzzleData)

    def __str__(self):
        return "Player "+self.name+" Id:"+self.social_id + str(self.puzzle_data)