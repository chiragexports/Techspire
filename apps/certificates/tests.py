from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.courses.models import CourseCategory, Course, Module, Lesson, CourseReview
from apps.enrollments.models import Enrollment, LessonProgress
from apps.quizzes.models import Quiz, Question, Choice, QuizAttempt
from apps.certificates.models import Certificate
from apps.certificates.pdf_generator import generate_certificate_pdf_buffer

User = get_user_model()

class ComprehensiveLMSTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Create User
        self.user = User.objects.create_user(
            username="student_test@techspire.in",
            email="student_test@techspire.in",
            password="TestPassword123",
            first_name="Aarav",
            last_name="Gupta",
            role="student"
        )

        # 2. Create Category & Course
        self.cat = CourseCategory.objects.create(name="Python Programming", slug="python-programming")
        self.course = Course.objects.create(
            title="Python Testing Masterclass",
            slug="python-testing-masterclass",
            category=self.cat,
            instructor=self.user,
            short_description="Short desc",
            description="Full desc",
            is_free=True,
            is_published=True
        )

        # 3. Create Module & Lessons
        self.mod = Module.objects.create(course=self.course, title="Module 1", order=1)
        self.l1 = Lesson.objects.create(module=self.mod, title="Lesson 1", order=1, content="Lesson 1 content")
        self.l2 = Lesson.objects.create(module=self.mod, title="Lesson 2", order=2, content="Lesson 2 content")

        # 4. Create Quiz & Questions
        self.quiz = Quiz.objects.create(
            course=self.course,
            title="Course Final Assessment",
            pass_percentage=70,
            is_published=True
        )
        self.q1 = Question.objects.create(quiz=self.quiz, prompt="What is Python?", points=1, order=1)
        self.c1 = Choice.objects.create(question=self.q1, choice_text="Programming Language", is_correct=True)
        self.c2 = Choice.objects.create(question=self.q1, choice_text="Snake Species Only", is_correct=False)

    def test_complete_lms_workflow(self):
        # 1. Login
        logged_in = self.client.login(username="student_test@techspire.in", password="TestPassword123")
        self.assertTrue(logged_in)

        # 2. Course Catalog & Detail View
        catalog_res = self.client.get(reverse('courses:course_list'))
        self.assertEqual(catalog_res.status_code, 200)
        self.assertContains(catalog_res, "Python Testing Masterclass")

        detail_res = self.client.get(reverse('courses:course_detail', kwargs={'slug': self.course.slug}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, "Course Curriculum")

        # 3. Enroll in Course
        enroll_response = self.client.get(reverse('enrollments:enroll', kwargs={'slug': self.course.slug}), follow=True)
        self.assertEqual(enroll_response.status_code, 200)
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())
        enrollment = Enrollment.objects.get(user=self.user, course=self.course)

        # 4. Student Dashboard & My Courses View
        dash_res = self.client.get(reverse('dashboard:student_dashboard'))
        self.assertEqual(dash_res.status_code, 200)
        self.assertContains(dash_res, "STUDENT LEARNING PORTAL")

        my_courses_res = self.client.get(reverse('dashboard:my_courses'))
        self.assertEqual(my_courses_res.status_code, 200)
        self.assertContains(my_courses_res, "Python Testing Masterclass")

        # 5. Complete Lessons
        self.client.post(reverse('enrollments:mark_complete', kwargs={'course_slug': self.course.slug, 'lesson_id': self.l1.id}), follow=True)
        self.client.post(reverse('enrollments:mark_complete', kwargs={'course_slug': self.course.slug, 'lesson_id': self.l2.id}), follow=True)
        
        self.assertEqual(enrollment.progress_percentage, 100)

        # 6. Take and Pass Quiz
        quiz_submit_res = self.client.post(
            reverse('quizzes:take_quiz', kwargs={'quiz_id': self.quiz.id}),
            {f"question_{self.q1.id}": self.c1.id},
            follow=True
        )
        self.assertEqual(quiz_submit_res.status_code, 200)
        self.assertTrue(QuizAttempt.objects.filter(user=self.user, quiz=self.quiz, passed=True).exists())

        # 7. Verify Certificate Generated
        cert = Certificate.objects.filter(user=self.user, course=self.course).first()
        self.assertIsNotNone(cert)
        self.assertTrue(cert.certificate_id.startswith("TS-2026-"))

        # 8. Verify PDF buffer generation and download endpoint
        pdf_buffer = generate_certificate_pdf_buffer(cert)
        self.assertGreater(len(pdf_buffer.getvalue()), 1000)

        download_res = self.client.get(reverse('certificates:download_pdf', kwargs={'cert_id': cert.certificate_id}))
        self.assertEqual(download_res.status_code, 200)
        self.assertEqual(download_res['Content-Type'], 'application/pdf')

        # 9. Test Public Certificate Verification Portal
        verify_res = self.client.get(f"{reverse('certificates:verify_public')}?cert_id={cert.certificate_id}")
        self.assertEqual(verify_res.status_code, 200)
        self.assertContains(verify_res, "OFFICIALLY VERIFIED")
        self.assertContains(verify_res, "Aarav Gupta")
        self.assertContains(verify_res, "Python Testing Masterclass")

        # 10. Add Course Review
        review_res = self.client.post(
            reverse('courses:add_review', kwargs={'slug': self.course.slug}),
            {'rating': 5, 'comment': 'Outstanding course! Highly recommended.'},
            follow=True
        )
        self.assertEqual(review_res.status_code, 200)
        self.assertTrue(CourseReview.objects.filter(course=self.course, user=self.user).exists())
