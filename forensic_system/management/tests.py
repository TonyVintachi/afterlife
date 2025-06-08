from django.test import TestCase
from django.utils import timezone
from django.urls import reverse # 'resolve' might not be needed for basic view tests
from django.contrib.auth import get_user_model
from .models import Case, Body, RFIDTag, AutopsyReport # Add AutopsyReport
from . import views # Import views for view tests, not strictly needed for resolve(url).func with reverse

User = get_user_model()

class CaseModelTests(TestCase):
    def test_create_case(self): # test_create_case_with_autopsy_details is removed
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

class RFIDTagModelTests(TestCase): # Preserved
    def test_create_rfid_tag(self):
        tag = RFIDTag.objects.create(
            tag_id="RFID001",
            status="active"
        )
        self.assertEqual(tag.tag_id, "RFID001")
        self.assertEqual(tag.status, "active")
        self.assertEqual(str(tag), "RFID Tag RFID001")

class AutopsyReportModelTests(TestCase): # New Test Class
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
        retrieved_report = AutopsyReport.objects.get(id=report.id) # Fetch from DB to ensure save
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


class BodyModelTests(TestCase): # Preserved
    def setUp(self):
        self.case = Case.objects.create(case_number="CASEBODY01", type_of_case="autopsy")
        self.rfid_tag = RFIDTag.objects.create(tag_id="RFIDBODY01")

    def test_create_body(self):
        body = Body.objects.create(
            body_uid="BODY001",
            name="John Doe",
            date_of_death=timezone.now().date(),
            case=self.case,
            rfid_tag=self.rfid_tag
        )
        self.assertEqual(body.body_uid, "BODY001")
        self.assertEqual(body.name, "John Doe")
        self.assertEqual(body.case, self.case)
        self.assertEqual(body.rfid_tag, self.rfid_tag)
        self.assertEqual(str(body), "Body BODY001 (John Doe)")

    def test_create_body_unknown_name(self):
        body = Body.objects.create(
            body_uid="BODY002",
            case=self.case
        )
        self.assertEqual(body.body_uid, "BODY002")
        self.assertIsNone(body.name)
        self.assertEqual(str(body), "Body BODY002 (Unknown)")

    def test_body_rfid_tag_optional(self):
        body = Body.objects.create(
            body_uid="BODY003",
            case=self.case
        )
        self.assertEqual(body.body_uid, "BODY003")
        self.assertIsNone(body.rfid_tag)


class AutopsyReportViewTests(TestCase): # Updated Test Class
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
        self.body_associated = Body.objects.create(
            body_uid="VIEWBODY01",
            name="View Victim",
            case=self.case_with_report
        )
        self.case_without_report = Case.objects.create(case_number="VIEWCASE02", type_of_case="other")

    def test_autopsy_report_detail_view_success_status_code(self):
        url = reverse('management:autopsy_report_detail', args=[self.case_with_report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_autopsy_report_detail_view_not_found_status_code(self):
        url = reverse('management:autopsy_report_detail', args=[999]) # Non-existent Case ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_autopsy_report_detail_view_uses_correct_template(self):
        url = reverse('management:autopsy_report_detail', args=[self.case_with_report.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'management/autopsy_report_detail.html')

    def test_autopsy_report_detail_view_displays_report_information(self):
        url = reverse('management:autopsy_report_detail', args=[self.case_with_report.id])
        response = self.client.get(url)
        self.assertContains(response, self.case_with_report.case_number) # Case info
        self.assertContains(response, self.report.pathologist_name)
        self.assertContains(response, self.report.cause_of_death_preliminary)
        self.assertContains(response, self.report.external_examination_summary)
        self.assertContains(response, self.report.internal_examination_summary)
        self.assertContains(response, self.report.toxicology_specimens_taken)
        self.assertContains(response, self.report.histology_specimens_taken)
        self.assertContains(response, self.report.autopsy_notes)
        self.assertContains(response, self.autopsy_time.strftime('%Y-%m-%d')) # Formatted date
        self.assertContains(response, self.user.username)
        self.assertContains(response, "Yes") # For is_finalized=True
        self.assertContains(response, self.body_associated.name) # Associated body

    def test_autopsy_report_view_no_report_object(self): # New test
        url = reverse('management:autopsy_report_detail', args=[self.case_without_report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No autopsy report details available for this case.")
        # Check that specific report data is NOT present
        self.assertNotContains(response, "Pathologist:")
        self.assertNotContains(response, "Dr. View Test") # Example data from other test's report
        self.assertNotContains(response, "View External Summary")
