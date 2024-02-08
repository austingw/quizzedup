from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django import forms
from django.core.paginator import Paginator
from .models import Trivia, UserScores

import requests


@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        response = requests.get("https://opentdb.com/api.php?amount=1&type=boolean")
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            question = data['results'][0]  # Extract the first question
        else:
            return HttpResponse('Error: No results from the Open Trivia Database, wait a few seconds and refresh.')
    elif request.method == 'POST':
        question = request.POST.get('question')  # Retrieve the current question from the POST data
        if not question:
            return HttpResponse('Error: No current question in POST data')
    else:
        return HttpResponse('Invalid request')

    return render(request, 'index.html', {'question': question})

def answer(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        user_answer = request.POST.get('user_answer')
        correct_answer = request.POST.get('correct_answer')
        print(question, user_answer, correct_answer)
        if question is None or user_answer is None or correct_answer is None:
            return HttpResponse('Invalid request')

        correct = user_answer == correct_answer

        try:
            user_score = UserScores.objects.get(user=request.user)
        except UserScores.DoesNotExist:
            user_score = UserScores(user=request.user)

        if correct:
            user_score.score += 1

        user_score.save()

        trivia = Trivia(question=question, answer=correct_answer, correct=correct, user=request.user)
        trivia.save()

        return render(request, 'partials/answered.html', {'correct': correct, 'answer': correct_answer, 'question': question})

    else:
        return HttpResponse('Invalid request')

def new_question(request):
    response = requests.get("https://opentdb.com/api.php?amount=1&type=boolean")
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        question = data['results'][0]  # Extract the first question
        return render(request, 'partials/new_question.html', {'question': question})
    else:
        return JsonResponse({'error': 'No results from the Open Trivia Database, wait a few seconds and refresh.'})

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'form_type': 'login'})

def custom_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, 'form_type': 'signup'})
    
def leaderboard(request):
    scores = UserScores.objects.all().order_by('-score')

    return render(request, 'leaderboard.html', {'scores': scores})