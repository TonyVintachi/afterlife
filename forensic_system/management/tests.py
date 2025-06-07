from django.test import TestCase
from django.utils import timezone
from .models import Case, Body, RFIDTag

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
