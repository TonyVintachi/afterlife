from django.shortcuts import render, get_object_or_404 # Ensure get_object_or_404 is imported
from django.http import HttpResponse
from .models import Case # Ensure Case model is imported

def homepage(request):
    return render(request, 'management/homepage.html', {'message': 'Welcome to the Forensic Information Management System'})

def autopsy_report_detail_view(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    # We can add more context here if needed, e.g., related bodies
    context = {
        'case': case,
    }
    return render(request, 'management/autopsy_report_detail.html', context)
