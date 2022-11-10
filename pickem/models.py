import uuid
from django.db import models
from django.conf import settings

GROUP_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("G", "G"),
    ("H", "H"),
)

KNOCKOUT_CHOICES = (
    ("Octavos", "Octavos"),
    ("Cuartos", "Cuartos"),
    ("Semis", "Semis"),
    ("Tercero", "Tercero"),
    ("Final", "Final"),
)

QUESTION_CHOICES = (
    ("Player", "Player"),
    ("Team", "Team"),
    ("Misc", "Misc"),
)

ONE = 1
TWO = 2
THREE = 3
FOUR = 4
RANKING_CHOICES = (
    (ONE, 'Primero'),
    (TWO, 'Segundo'),
    (THREE, 'Tercero'),
    (FOUR, 'Cuarto'),
)

class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True)
    photo = models.CharField(max_length=1000, blank=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.player_name

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_name = models.CharField(max_length=30)
    final_group_position = models.IntegerField(default=0, blank=True)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)

    def __str__(self):
        return self.team_name

class UserGroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    ranking = models.IntegerField(choices=RANKING_CHOICES)

    class Meta:
        unique_together = (('user', 'group', 'ranking'), ('user', 'team'))


class UserKnockout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phase = models.CharField(max_length=10, choices=KNOCKOUT_CHOICES)
    team_a = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_a_knockout')
    team_b = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_b_knockout')
    winner = models.BooleanField()


class Knockout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phase = models.CharField(max_length=30)
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        return self.phase + " " + self.teams

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=30, choices=QUESTION_CHOICES)
    value = models.IntegerField()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice_player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True)
    choice_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)
    choice_text = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.question.question_text
