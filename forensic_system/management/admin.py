from django.contrib import admin
from .models import Case, Body, RFIDTag

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'type_of_case', 'date_reported', 'current_status', 'autopsy_date', 'pathologist_name', 'cause_of_death_preliminary')
    list_filter = ('type_of_case', 'current_status', 'date_reported', 'autopsy_date')
    search_fields = ('case_number', 'pathologist_name')

    fieldsets = (
        (None, {
            'fields': ('case_number', 'type_of_case', 'date_reported', 'current_status')
        }),
        ('Autopsy Details', {
            'classes': ('collapse',), # Collapsible section
            'fields': ('autopsy_date', 'pathologist_name', 'cause_of_death_preliminary', 'autopsy_notes')
        }),
    )

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('body_uid', 'name', 'case', 'rfid_tag', 'date_of_death')
    list_filter = ('date_of_death',)
    search_fields = ('body_uid', 'name', 'case__case_number', 'rfid_tag__tag_id')
    raw_id_fields = ('case', 'rfid_tag') # Useful for foreign keys with many entries

@admin.register(RFIDTag)
class RFIDTagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'status')
    list_filter = ('status',)
    search_fields = ('tag_id',)
