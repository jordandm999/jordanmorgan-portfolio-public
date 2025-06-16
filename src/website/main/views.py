from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def chatbot(request):
    return render(request, 'main/chatbot.html')