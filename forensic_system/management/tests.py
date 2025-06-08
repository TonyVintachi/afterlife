from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Case, Body, RFIDTag, AutopsyReport
from . import views

User = get_user_model()

class CaseModelTests(TestCase):
    def test_create_case(self):
        case = Case.objects.create(
            case_number="CASE001",
            type_of_case="autopsy",
            current_status="Pending"
        )
        self.assertEqual(case.case_number, "CASE001")
        self.assertEqual(case.type_of_case, "autopsy")
        self.assertEqual(case.current_status, "Pending")
        self.assertTrue(case.date_reported)
        self.assertEqual(str(case), "Case CASE001")

class RFIDTagModelTests(TestCase):
    def test_create_rfid_tag(self):
        tag = RFIDTag.objects.create(
            tag_id="RFID001",
            status="active"
        )
        self.assertEqual(tag.tag_id, "RFID001")
        self.assertEqual(tag.status, "active")
        self.assertEqual(str(tag), "RFID Tag RFID001")

class AutopsyReportModelTests(TestCase):
    def setUp(self):
        self.case_instance = Case.objects.create(case_number="AR_CASE01", type_of_case="autopsy")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.autopsy_time = timezone.now().date()

    def test_create_autopsy_report(self):
        report = AutopsyReport.objects.create(
            case=self.case_instance,
            autopsy_date=self.autopsy_time,
            pathologist_name="Dr. Test Pathologist",
            cause_of_death_preliminary="Test Cause",
            autopsy_notes="Test notes.",
            external_examination_summary="External summary.",
            internal_examination_summary="Internal summary.",
            toxicology_specimens_taken="Blood, Urine.",
            histology_specimens_taken="Liver, Kidney.",
            report_finalized_by=self.user,
            is_finalized=True
        )
        retrieved_report = AutopsyReport.objects.get(id=report.id)
        self.assertEqual(retrieved_report.case, self.case_instance)
        self.assertEqual(retrieved_report.pathologist_name, "Dr. Test Pathologist")
        self.assertEqual(retrieved_report.external_examination_summary, "External summary.")
        self.assertEqual(retrieved_report.internal_examination_summary, "Internal summary.")
        self.assertEqual(retrieved_report.toxicology_specimens_taken, "Blood, Urine.")
        self.assertEqual(retrieved_report.histology_specimens_taken, "Liver, Kidney.")
        self.assertTrue(retrieved_report.date_report_generated)
        self.assertTrue(retrieved_report.is_finalized)
        self.assertEqual(retrieved_report.report_finalized_by, self.user)
        self.assertEqual(str(retrieved_report), f"Autopsy Report for Case {self.case_instance.case_number}")

class BodyModelTests(TestCase):
    def setUp(self):
        self.case = Case.objects.create(case_number="CASEBODY01", type_of_case="autopsy")
        self.rfid_tag = RFIDTag.objects.create(tag_id="RFIDBODY01")

    def test_create_body_with_all_details(self): # Modified to include new fields
        body_creation_time = timezone.now().date()
        body = Body.objects.create(
            body_uid="BODY001",
            name="John Doe",
            date_of_death=body_creation_time,
            case=self.case,
            rfid_tag=self.rfid_tag,
            # New fields
            fingerprint_scan_ref="path/to/fingerprints_001.tiff",
            dental_records_ref="path/to/dental_001.pdf",
            dna_sample_id="DNA001X",
            dha_identification_status='IDENTIFIED', # Test with IDENTIFIED
            dha_id_number="8001015000080",
            dha_response_notes="Positive ID match from DHA."
        )
        retrieved_body = Body.objects.get(id=body.id)
        self.assertEqual(retrieved_body.body_uid, "BODY001")
        self.assertEqual(retrieved_body.name, "John Doe")
        self.assertEqual(retrieved_body.case, self.case)
        self.assertEqual(retrieved_body.rfid_tag, self.rfid_tag)
        self.assertEqual(retrieved_body.date_of_death, body_creation_time)

        self.assertEqual(retrieved_body.fingerprint_scan_ref, "path/to/fingerprints_001.tiff")
        self.assertEqual(retrieved_body.dental_records_ref, "path/to/dental_001.pdf")
        self.assertEqual(retrieved_body.dna_sample_id, "DNA001X")
        self.assertEqual(retrieved_body.dha_identification_status, 'IDENTIFIED')
        self.assertEqual(retrieved_body.dha_id_number, "8001015000080")
        self.assertEqual(retrieved_body.dha_response_notes, "Positive ID match from DHA.")
        self.assertEqual(str(retrieved_body), "Body BODY001 (John Doe)")

    def test_create_body_unknown_name(self): # Unchanged
        body = Body.objects.create(
            body_uid="BODY002",
            case=self.case
        )
        self.assertEqual(body.body_uid, "BODY002")
        self.assertIsNone(body.name)
        self.assertEqual(str(body), "Body BODY002 (Unknown)")

    def test_body_rfid_tag_optional(self): # Unchanged
        body = Body.objects.create(
            body_uid="BODY003",
            case=self.case
        )
        self.assertEqual(body.body_uid, "BODY003")
        self.assertIsNone(body.rfid_tag)

class AutopsyReportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testviewer', password='password')
        self.case_with_report = Case.objects.create(case_number="VIEWCASE01", type_of_case="autopsy")
        self.autopsy_time = timezone.now().date()
        self.report = AutopsyReport.objects.create(
            case=self.case_with_report,
            autopsy_date=self.autopsy_time,
            pathologist_name="Dr. View Test",
            cause_of_death_preliminary="View Test Cause",
            external_examination_summary="View External Summary",
            internal_examination_summary="View Internal Summary",
            toxicology_specimens_taken="Specimens A, B",
            histology_specimens_taken="Tissues X, Y",
            autopsy_notes="Detailed view notes.",
            report_finalized_by=self.user,
            is_finalized=True
        )
        # Body that is identified
        self.body_associated_identified = Body.objects.create(
            body_uid="VIEWBODY_ID",
            name="Identified Victim",
            case=self.case_with_report,
            fingerprint_scan_ref="prints/id_victim.tiff",
            dental_records_ref="dental/id_victim.pdf",
            dna_sample_id="DNA_ID_VIC",
            dha_identification_status='IDENTIFIED',
            dha_id_number="8001015000080",
            dha_response_notes="Positive ID match from DHA."
        )
        # Body that is pending DHA identification
        self.body_associated_pending = Body.objects.create(
            body_uid="VIEWBODY_PEND",
            name="Pending Victim",
            case=self.case_with_report,
            dha_identification_status='PENDING_DHA',
            dna_sample_id="DNA_PEND_VIC" # Added some data to distinguish
        )
        self.case_without_report = Case.objects.create(case_number="VIEWCASE02", type_of_case="other")

    def test_autopsy_report_detail_view_success_status_code(self):
        url = reverse('management:autopsy_report_detail', args=[self.case_with_report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_autopsy_report_detail_view_not_found_status_code(self):
        url = reverse('management:autopsy_report_detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_autopsy_report_detail_view_uses_correct_template(self):
        url = reverse('management:autopsy_report_detail', args=[self.case_with_report.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'management/autopsy_report_detail.html')

    def test_autopsy_report_detail_view_displays_autopsy_report_info(self): # Focused name
        url = reverse('management:autopsy_report_detail', args=[self.case_with_report.id])
        response = self.client.get(url)
        self.assertContains(response, self.case_with_report.case_number)
        self.assertContains(response, self.report.pathologist_name)
        self.assertContains(response, self.report.cause_of_death_preliminary)
        self.assertContains(response, self.report.external_examination_summary)
        # ... (can add more assertions for other AutopsyReport fields if desired)
        self.assertContains(response, self.autopsy_time.strftime('%Y-%m-%d'))
        self.assertContains(response, self.user.username)
        self.assertContains(response, "Yes") # For is_finalized=True

    def test_autopsy_report_detail_view_displays_body_dha_info(self): # New focused test
        url = reverse('management:autopsy_report_detail', args=[self.case_with_report.id])
        response = self.client.get(url)

        # Test for identified body
        self.assertContains(response, self.body_associated_identified.body_uid)
        self.assertContains(response, self.body_associated_identified.name)
        self.assertContains(response, self.body_associated_identified.fingerprint_scan_ref)
        self.assertContains(response, self.body_associated_identified.dental_records_ref)
        self.assertContains(response, self.body_associated_identified.dna_sample_id)
        self.assertContains(response, self.body_associated_identified.get_dha_identification_status_display())
        self.assertContains(response, self.body_associated_identified.dha_id_number) # Should be displayed

        # Test for pending body
        self.assertContains(response, self.body_associated_pending.body_uid)
        self.assertContains(response, self.body_associated_pending.name)
        self.assertContains(response, self.body_associated_pending.dna_sample_id) # Check one of its unique fields
        self.assertContains(response, self.body_associated_pending.get_dha_identification_status_display())
        if self.body_associated_pending.dha_id_number: # Only assertNotContains if it has a value
             self.assertNotContains(response, self.body_associated_pending.dha_id_number)
        else: # If it's None or empty, check that a placeholder like "Not Provided" isn't shown outside the IDENTIFIED block
            self.assertNotContains(response, "Not Provided") # Assuming this is the default in the template if status isn't IDENTIFIED

        # Check for action placeholders for at least one body (they are identical for all)
        self.assertContains(response, "[Simulate DHA Identification Request]")
        self.assertContains(response, "[Enter DHA Response]")


    def test_autopsy_report_view_no_report_object(self):
        url = reverse('management:autopsy_report_detail', args=[self.case_without_report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No autopsy report details available for this case.")
        self.assertNotContains(response, "Pathologist:")
        self.assertNotContains(response, "Dr. View Test")
        self.assertNotContains(response, "View External Summary")
