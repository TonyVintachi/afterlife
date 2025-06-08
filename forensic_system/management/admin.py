from django.contrib import admin
from .models import Case, Body, RFIDTag, AutopsyReport # Add AutopsyReport

# Inline Admin for AutopsyReport
class AutopsyReportInline(admin.StackedInline): # Or admin.TabularInline for a more compact view
    model = AutopsyReport
    can_delete = False # Usually, an autopsy report is integral to a case
    verbose_name_plural = 'Autopsy Report Details'
    fk_name = 'case' # Explicitly state the foreign key name

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
            'classes': ('collapse',), # Collapsible section
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
                'report_finalized_by', # This will be a dropdown for users
                'date_report_generated',
            )
        })
    )
    readonly_fields = ('date_report_generated',) # This is auto-set

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'type_of_case', 'date_reported', 'current_status') # Old autopsy fields removed
    list_filter = ('type_of_case', 'current_status', 'date_reported')
    search_fields = ('case_number',) # Old pathologist_name removed

    # Fieldsets for Case model's own fields
    fieldsets = (
        (None, {
            'fields': ('case_number', 'type_of_case', 'date_reported', 'current_status')
        }),
    )

    inlines = [AutopsyReportInline] # Add the inline here

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('body_uid', 'name', 'case', 'rfid_tag', 'date_of_death')
    list_filter = ('date_of_death',)
    search_fields = ('body_uid', 'name', 'case__case_number', 'rfid_tag__tag_id')
    raw_id_fields = ('case', 'rfid_tag')

@admin.register(RFIDTag)
class RFIDTagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'status')
    list_filter = ('status',)
    search_fields = ('tag_id',)

# Optional: Direct registration for AutopsyReport if needed for standalone access/management
# @admin.register(AutopsyReport)
# class AutopsyReportAdmin(admin.ModelAdmin):
#     list_display = ('case', 'autopsy_date', 'pathologist_name', 'is_finalized')
#     list_filter = ('is_finalized', 'autopsy_date')
#     search_fields = ('case__case_number', 'pathologist_name')
#     raw_id_fields = ('case', 'report_finalized_by')
