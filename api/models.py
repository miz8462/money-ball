from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return self.team_name


class Player(models.Model):
    name = models.CharField(max_length=50)
    born = models.DateField(default="2000-01-01")
    height = models.IntegerField(default=180)
    weight = models.IntegerField(default=80)
    salary = models.IntegerField(default=1000)  # 万円
    uniform_number = models.IntegerField(default=0)
    team = models.ForeignKey(Team, related_name="players", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
