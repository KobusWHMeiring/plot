from django.test import TestCase

from core.models import PilotInquiry


class CaseStudyRoutingTests(TestCase):
    def test_case_study_pages_return_200(self):
        for slug in ('harvester', 'river', 'farm'):
            with self.subTest(slug=slug):
                response = self.client.get(f'/work/{slug}/')
                self.assertEqual(response.status_code, 200)

    def test_unknown_case_study_returns_404(self):
        response = self.client.get('/work/unknown/')
        self.assertEqual(response.status_code, 404)

    def test_home_returns_200(self):
        self.assertEqual(self.client.get('/').status_code, 200)


class InquiryFlowTests(TestCase):
    def test_valid_post_creates_inquiry(self):
        response = self.client.post(
            '/submit-inquiry/',
            {'name': 'Jane', 'email': 'jane@example.com', 'message': 'Hi'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PilotInquiry.objects.filter(email='jane@example.com').exists())

    def test_missing_fields_return_400(self):
        response = self.client.post('/submit-inquiry/', {'name': '', 'email': ''})
        self.assertEqual(response.status_code, 400)
