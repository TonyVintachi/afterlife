from django.test import TestCase
from django.utils import timezone
from django.urls import reverse, resolve # Added reverse and resolve
from .models import Case, Body, RFIDTag
from . import views # Added views import

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
        self.assertTrue(case.date_reported) # Should be set by default
        self.assertEqual(str(case), "Case CASE001")

    def test_create_case_with_autopsy_details(self):
        autopsy_time = timezone.now().date()
        case = Case.objects.create(
            case_number="CASEAUTO001",
            type_of_case="autopsy",
            current_status="Autopsy Complete",
            autopsy_date=autopsy_time,
            pathologist_name="Dr. Smith",
            cause_of_death_preliminary="Multiple blunt force trauma",
            autopsy_notes="Detailed notes here."
        )
        self.assertEqual(case.autopsy_date, autopsy_time)
        self.assertEqual(case.pathologist_name, "Dr. Smith")
        self.assertEqual(case.cause_of_death_preliminary, "Multiple blunt force trauma")
        self.assertEqual(case.autopsy_notes, "Detailed notes here.")

class RFIDTagModelTests(TestCase):
    def test_create_rfid_tag(self):
        tag = RFIDTag.objects.create(
            tag_id="RFID001",
            status="active"
        )
        self.assertEqual(tag.tag_id, "RFID001")
        self.assertEqual(tag.status, "active")
        self.assertEqual(str(tag), "RFID Tag RFID001")

class BodyModelTests(TestCase):
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
            # Name is optional
        )
        self.assertEqual(body.body_uid, "BODY002")
        self.assertIsNone(body.name)
        self.assertEqual(str(body), "Body BODY002 (Unknown)")

    def test_body_rfid_tag_optional(self):
        body = Body.objects.create(
            body_uid="BODY003",
            case=self.case
            # RFID tag is optional
        )
        self.assertEqual(body.body_uid, "BODY003")
        self.assertIsNone(body.rfid_tag)

class AutopsyReportViewTests(TestCase):
    def setUp(self):
        self.autopsy_time = timezone.now().date()
        self.case = Case.objects.create(
            case_number="AUTOPSYCASE01",
            type_of_case="autopsy",
            autopsy_date=self.autopsy_time,
            pathologist_name="Dr. Jane Doe",
            cause_of_death_preliminary="Asphyxiation",
            autopsy_notes="Notes regarding asphyxiation."
        )
        # Create a body associated with this case
        self.body = Body.objects.create(
            body_uid="BODYAUTO01",
            case=self.case,
            name="Victim One"
        )

    def test_autopsy_report_detail_url_resolves(self):
        url = reverse('management:autopsy_report_detail', args=[self.case.id])
        self.assertEqual(resolve(url).func, views.autopsy_report_detail_view)

    def test_autopsy_report_detail_view_success_status_code(self):
        url = reverse('management:autopsy_report_detail', args=[self.case.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_autopsy_report_detail_view_not_found_status_code(self):
        url = reverse('management:autopsy_report_detail', args=[999]) # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_autopsy_report_detail_view_uses_correct_template(self):
        url = reverse('management:autopsy_report_detail', args=[self.case.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'management/autopsy_report_detail.html')

    def test_autopsy_report_detail_view_displays_case_information(self):
        url = reverse('management:autopsy_report_detail', args=[self.case.id])
        response = self.client.get(url)
        self.assertContains(response, self.case.case_number)
        self.assertContains(response, self.case.pathologist_name)
        self.assertContains(response, self.case.cause_of_death_preliminary)
        self.assertContains(response, self.body.name) # Check if associated body name is present
        self.assertContains(response, self.autopsy_time.strftime('%Y-%m-%d'))
