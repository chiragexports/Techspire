from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import SiteSetting, FAQ, ContactInquiry

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        SiteSetting.objects.create(
            brand_name="TECHSPIRE Learning",
            business_name="TECHSPIRE",
            proprietor_name="Vivek Jat"
        )
        FAQ.objects.create(question="Is it online?", answer="Yes, 100% online.", is_active=True)

    def test_home_page(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TECHSPIRE")
        self.assertContains(response, "Learn Today, Lead Tomorrow")

    def test_about_page(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vivek Jat")
        self.assertContains(response, "Indore")

    def test_contact_submission(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '9876543210',
            'subject': 'Admission Inquiry',
            'message': 'I would like to know more about Python course.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactInquiry.objects.filter(email='test@example.com').exists())
