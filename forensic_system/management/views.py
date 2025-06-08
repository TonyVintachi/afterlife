from django.shortcuts import render, get_object_or_404
from .models import Case, AutopsyReport, ToxicologyReport # Add ToxicologyReport

def homepage(request):
    return render(request, 'management/homepage.html', {'message': 'Welcome to the Forensic Information Management System'})

def autopsy_report_detail_view(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    autopsy_report_obj = None
    try:
        autopsy_report_obj = case.autopsy_report # Accessing via related_name
    except AutopsyReport.DoesNotExist:
        pass # autopsy_report_obj remains None, template will handle
    context = {
        'case': case,
        'autopsy_report': autopsy_report_obj,
    }
    return render(request, 'management/autopsy_report_detail.html', context)

def toxicology_report_list_view(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    reports = ToxicologyReport.objects.filter(case=case).order_by('-report_date', '-id')
    context = {
        'case': case,
        'reports': reports,
    }
    return render(request, 'management/toxicology_report_list.html', context)

def toxicology_report_detail_view(request, report_id):
    report = get_object_or_404(ToxicologyReport, pk=report_id)
    context = {
        'report': report,
    }
    return render(request, 'management/toxicology_report_detail.html', context)
