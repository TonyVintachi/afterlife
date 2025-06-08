from django.contrib import admin
from .models import Case, Body, RFIDTag, AutopsyReport # AutopsyReport already imported

# Inline Admin for AutopsyReport (Unchanged from previous step)
class AutopsyReportInline(admin.StackedInline):
    model = AutopsyReport
    can_delete = False
    verbose_name_plural = 'Autopsy Report Details'
    fk_name = 'case'
    fieldsets = (
        (None, {
            'fields': (
                'autopsy_date',
                'pathologist_name',
                'cause_of_death_preliminary',
                'autopsy_notes'
            )
        }),
        ('Detailed Findings', {
            'classes': ('collapse',),
            'fields': (
                'external_examination_summary',
                'internal_examination_summary',
                'toxicology_specimens_taken',
                'histology_specimens_taken'
            )
        }),
        ('Report Status', {
            'fields': (
                'is_finalized',
                'report_finalized_by',
                'date_report_generated',
            )
        })
    )
    readonly_fields = ('date_report_generated',)

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin): # Unchanged from previous step
    list_display = ('case_number', 'type_of_case', 'date_reported', 'current_status')
    list_filter = ('type_of_case', 'current_status', 'date_reported')
    search_fields = ('case_number',)
    fieldsets = (
        (None, {
            'fields': ('case_number', 'type_of_case', 'date_reported', 'current_status')
        }),
    )
    inlines = [AutopsyReportInline]

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin): # Updated
    list_display = ('body_uid', 'name', 'case', 'rfid_tag', 'date_of_death', 'dha_identification_status', 'dha_id_number')
    list_filter = ('date_of_death', 'dha_identification_status') # Added dha_identification_status
    search_fields = ('body_uid', 'name', 'case__case_number', 'rfid_tag__tag_id', 'dha_id_number') # Added dha_id_number
    raw_id_fields = ('case', 'rfid_tag')

    fieldsets = (
        ('Core Information', {
            'fields': ('body_uid', 'name', 'case', 'rfid_tag', 'date_of_death')
        }),
        ('Biometric & DHA Identification', {
            'classes': ('collapse',), # Collapsible section
            'fields': (
                'fingerprint_scan_ref',
                'dental_records_ref',
                'dna_sample_id',
                'dha_identification_status',
                'dha_id_number',
                'dha_response_notes'
            )
        }),
    )

@admin.register(RFIDTag)
class RFIDTagAdmin(admin.ModelAdmin): # Unchanged
    list_display = ('tag_id', 'status')
    list_filter = ('status',)
    search_fields = ('tag_id',)

# AutopsyReport direct admin registration can remain commented out
# @admin.register(AutopsyReport)
# class AutopsyReportAdmin(admin.ModelAdmin):
#     list_display = ('case', 'autopsy_date', 'pathologist_name', 'is_finalized')
# ...
