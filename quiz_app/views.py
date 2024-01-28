from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from .models import UserScores

import requests


@login_required(login_url='/login/')
def index(request):
    response = requests.get("https://opentdb.com/api.php?amount=1&type=boolean")
    data = response.json()
    question = data['results'][0]  # Extract the first question
    return render(request, 'index.html', {'question': question})
    
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Invalid username or password')
    else:
        return render(request, 'login.html')

def leaderboard(request):
    scores = UserScores.objects.order_by('-score')  # Fetch the scores and order them in descending order
    paginator = Paginator(scores, 10)  # Create a Paginator object

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the scores for the current page

    return render(request, 'leaderboard.html', {'page_obj': page_obj})  # Pass the scores to the template