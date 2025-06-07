from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return render(request, 'management/homepage.html', {'message': 'Welcome to the Forensic Information Management System'})
