from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import User
from apps.courses.models import CourseCategory
from apps.notes.models import NotesProduct, NotesChapter, NotesOrder, Coupon

class NotesMarketplaceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='student@test.com',
            email='student@test.com',
            password='Password123!',
            first_name='Test',
            last_name='Student',
            role='student'
        )
        self.category = CourseCategory.objects.create(
            name='Python Programming',
            slug='python-programming',
            description='Learn Python'
        )
        self.product = NotesProduct.objects.create(
            title='Python Zero to Pro',
            slug='python-zero-to-pro',
            subtitle='Complete notes',
            short_description='Best python notes',
            full_description='Full description here',
            category=self.category,
            price=299.00,
            original_price=599.00,
            is_published=True,
        )
        self.ch1 = NotesChapter.objects.create(
            product=self.product,
            order=1,
            title='Chapter 1: Python Fundamentals',
            slug='ch-1-python-fundamentals',
            is_preview=True,
            content_markdown='# Python Fundamentals\nprint("Hello World")',
            read_time_mins=15,
        )
        self.ch2 = NotesChapter.objects.create(
            product=self.product,
            order=2,
            title='Chapter 2: Data Structures',
            slug='ch-2-data-structures',
            is_preview=False,
            content_markdown='# Data Structures\nSecret premium content',
            read_time_mins=20,
        )

    def test_notes_list_page(self):
        resp = self.client.get(reverse('notes:marketplace'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Python Zero to Pro')

    def test_notes_detail_page(self):
        resp = self.client.get(reverse('notes:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Python Zero to Pro')
        self.assertContains(resp, 'Chapter 1: Python Fundamentals')

    def test_free_preview_accessible_to_guest(self):
        resp = self.client.get(reverse('notes:reader_chapter', kwargs={'product_slug': self.product.slug, 'chapter_slug': self.ch1.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello World')

    def test_locked_chapter_blocks_unauthorized_guest(self):
        resp = self.client.get(reverse('notes:reader_chapter', kwargs={'product_slug': self.product.slug, 'chapter_slug': self.ch2.slug}))
        # Guest is redirected or preview locked
        self.assertNotEqual(resp.status_code, 200)

    def test_purchase_unlocks_locked_chapter(self):
        self.client.login(username='student@test.com', password='Password123!')
        
        # Grant purchase entitlement
        NotesOrder.objects.create(
            user=self.user,
            product=self.product,
            amount=299.00,
            status='paid',
            is_verified=True
        )
        
        resp = self.client.get(reverse('notes:reader_chapter', kwargs={'product_slug': self.product.slug, 'chapter_slug': self.ch2.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Secret premium content')

    def test_pdf_download_protection(self):
        # Guest cannot download PDF
        resp = self.client.get(reverse('notes:download_pdf', kwargs={'slug': self.product.slug}))
        self.assertNotEqual(resp.status_code, 200)

        # Logged in purchased user can download PDF
        self.client.login(username='student@test.com', password='Password123!')
        NotesOrder.objects.create(
            user=self.user,
            product=self.product,
            amount=299.00,
            status='paid',
            is_verified=True
        )
        resp = self.client.get(reverse('notes:download_pdf', kwargs={'slug': self.product.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/pdf')

    def test_my_notes_dashboard(self):
        self.client.login(username='student@test.com', password='Password123!')
        NotesOrder.objects.create(
            user=self.user,
            product=self.product,
            amount=299.00,
            status='paid',
            is_verified=True
        )
        resp = self.client.get(reverse('notes:my_notes'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Python Zero to Pro')
