from django.db import models
from django.utils import timezone

class Case(models.Model):
    case_number = models.CharField(max_length=100, unique=True)
    date_reported = models.DateTimeField(default=timezone.now)
    TYPE_CHOICES = [
        ('autopsy', 'Autopsy'),
        ('toxicology', 'Toxicology'),
        ('histology', 'Histology'),
        ('other', 'Other'),
    ]
    type_of_case = models.CharField(max_length=50, choices=TYPE_CHOICES)
    current_status = models.CharField(max_length=100, default='Pending Initial Examination')
    # Add more fields as needed, e.g., investigating_officer, police_station

    def __str__(self):
        return f"Case {self.case_number}"

class RFIDTag(models.Model):
    tag_id = models.CharField(max_length=100, unique=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('assigned', 'Assigned'),
        ('damaged', 'Damaged'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    # Add more fields as needed, e.g., last_scan_time, location

    def __str__(self):
        return f"RFID Tag {self.tag_id}"

class Body(models.Model):
    body_uid = models.CharField(max_length=100, unique=True, help_text="Unique Body Identifier")
    name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the deceased, if known")
    date_of_death = models.DateField(blank=True, null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='bodies')
    rfid_tag = models.OneToOneField(RFIDTag, on_delete=models.SET_NULL, blank=True, null=True, related_name='body')
    # Add more fields as needed, e.g., place_of_death, date_of_birth, sex, identifying_marks

    def __str__(self):
        return f"Body {self.body_uid} ({self.name or 'Unknown'})"
