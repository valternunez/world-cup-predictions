from django.shortcuts import render

from django.http import HttpResponse

from .models import Player, Knockout, Team, Question, Choice, UserGroup, UserKnockout, UserPoints

# Create your views here.
def index(request):
    return HttpResponse("Hello world. You're at the Pick'em index")


def calculate_team_group_points(user_team_group: UserGroup) -> int:
    user_points = UserPoints.objects.get(user=user_team_group.user)
    current_points = user_points.totalpoints
    team = Team.objects.get(id=user_team_group.team)
    final_position = team.final_group_position
    
    if user_team_group.ranking != final_position:
        pass # not sure if this will work tbh
    else:
        if final_position == 1 or final_position == 2:
            current_points = current_points + 5
        if final_position == 3 or final_position == 4:
            current_points = current_points + 2

    return current_points

def calculate_knockout_points(user_knockout: UserKnockout, knockout: Knockout) -> int:
    user_points = UserPoints.objects.get(user=user_knockout.user)
    current_points = user_points.totalpoints
    phase = knockout.phase
    winner = knockout.winner
    
    if phase == 'Octavos':
        awarded_points = 5
    elif phase == 'Cuartos':
        awarded_points = 10
    elif phase == 'Semis':
        awarded_points = 15
    elif phase == 'Tercero':
        awarded_points = 20
    elif phase == 'Final':
        awarded_points = 30
    
    if winner == user_knockout.winner:
        current_points = current_points + awarded_points
    
    return current_points

def calculate_question_points(user_choice: Choice, question: Question) -> int:
    user_points = UserPoints.objects.get(user=user_choice.user)
    current_points = user_points.totalpoints
    question_type = question.question_type
    
    if question_type == 'Player':
        if user_choice.choice_player == question.answer_player:
            current_points = current_points + question.value
    elif question_type == 'Team':
        if user_choice.choice_team == question.answer_team:
            current_points = current_points + question.value
    elif question_type == 'Misc':
        if user_choice.choice_text == question.answer_text:
            current_points = current_points + question.value
            
    return current_points
