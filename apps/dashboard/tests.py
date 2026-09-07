from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import User
from apps.courses.models import CourseCategory, Course, Module, Lesson
from apps.enrollments.models import Enrollment, LessonProgress
from apps.quizzes.models import Quiz, Question, Choice, QuizAttempt
from apps.core.models import ActivityLog

class AdminPortalAndProgressTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create Category
        self.category = CourseCategory.objects.create(
            name="Python Programming",
            slug="python-programming",
            icon_class="fab fa-python"
        )
        
        # Create Staff/Admin User
        self.admin_user = User.objects.create_superuser(
            username="admin_user",
            email="admin@techspire.in",
            password="AdminPassword123!",
            first_name="Admin",
            last_name="Manager",
            role="admin"
        )
        
        # Create Student User
        self.student_user = User.objects.create_user(
            username="student_alex",
            email="student@techspire.in",
            password="StudentPassword123!",
            first_name="Alex",
            last_name="Learner",
            role="student"
        )

        # Create Course
        self.course = Course.objects.create(
            category=self.category,
            title="Python Essentials 1",
            slug="python-essentials-1",
            short_description="Learn fundamentals of Python",
            description="Complete comprehensive course notes",
            level="beginner",
            duration_hours=12,
            is_free=True,
            is_published=True
        )

        # Create Module and Lessons
        self.module = Module.objects.create(
            course=self.course,
            title="Module 1: Introduction",
            order=1
        )
        self.lesson1 = Lesson.objects.create(
            module=self.module,
            title="1.1 Getting Started with Python",
            order=1,
            notes_markdown="# Getting Started\nPython is powerful.\n> [!TIP]\n> Practice daily.",
            duration_minutes=15
        )
        self.lesson2 = Lesson.objects.create(
            module=self.module,
            title="1.2 Data Types and Variables",
            order=2,
            notes_markdown="# Data Types\nIntegers and Strings.",
            duration_minutes=20
        )

        # Create Quiz
        self.quiz = Quiz.objects.create(
            course=self.course,
            title="Module 1 Checkpoint",
            pass_percentage=70,
            time_limit_minutes=10,
            is_published=True
        )
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            prompt="What is the output of type(42)?",
            points=1,
            order=1
        )
        self.choice1 = Choice.objects.create(
            question=self.q1,
            choice_text="<class 'int'>",
            is_correct=True
        )
        self.choice2 = Choice.objects.create(
            question=self.q1,
            choice_text="<class 'str'>",
            is_correct=False
        )

    def test_admin_portal_access_denied_for_students(self):
        """Ensure students cannot access admin portal endpoints and get redirected"""
        self.client.login(email="student@techspire.in", password="StudentPassword123!")
        
        # Overview redirects to student home
        response = self.client.get(reverse('dashboard:admin_overview'))
        self.assertEqual(response.status_code, 302)
        
        # Users list redirects
        response = self.client.get(reverse('dashboard:admin_users_list'))
        self.assertEqual(response.status_code, 302)

        # Export CSV redirects
        response = self.client.get(reverse('dashboard:admin_export_csv', kwargs={'report_type': 'users'}))
        self.assertEqual(response.status_code, 302)

    def test_admin_portal_access_granted_for_staff(self):
        """Ensure admin/staff can access the admin overview and directory"""
        self.client.login(email="admin@techspire.in", password="AdminPassword123!")
        
        response = self.client.get(reverse('dashboard:admin_overview'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Platform Administration & Analytics")
        self.assertContains(response, "Live Real-Time DB")

        response = self.client.get(reverse('dashboard:admin_users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex Learner")

    def test_student_enrollment_and_progress_tracking(self):
        """Test enrolling, viewing notes, updating progress, and sequential completion"""
        self.client.login(email="student@techspire.in", password="StudentPassword123!")
        
        # Enroll
        enroll_url = reverse('enrollments:enroll', kwargs={'slug': self.course.slug})
        response = self.client.get(enroll_url, follow=True)
        self.assertEqual(response.status_code, 200)
        
        enrollment = Enrollment.objects.get(user=self.student_user, course=self.course)
        self.assertEqual(enrollment.progress_percentage, 0)
        
        # View Lesson 1
        lesson_url = reverse('enrollments:lesson_view', kwargs={'course_slug': self.course.slug, 'lesson_id': self.lesson1.id})
        response = self.client.get(lesson_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Getting Started with Python")
        
        # Mark Lesson 1 complete
        complete_url = reverse('enrollments:mark_complete', kwargs={'course_slug': self.course.slug, 'lesson_id': self.lesson1.id})
        response = self.client.post(complete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.completed_lessons_count, 1)
        self.assertEqual(enrollment.progress_percentage, 50)
        # Advance pointer to lesson 2
        self.assertEqual(enrollment.last_accessed_lesson, self.lesson2)

        # Mark Lesson 2 complete
        complete_url2 = reverse('enrollments:mark_complete', kwargs={'course_slug': self.course.slug, 'lesson_id': self.lesson2.id})
        response = self.client.post(complete_url2, follow=True)
        self.assertEqual(response.status_code, 200)
        
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.completed_lessons_count, 2)
        self.assertEqual(enrollment.progress_percentage, 100)
        self.assertEqual(enrollment.status, 'completed')

    def test_quiz_attempt_and_activity_logging(self):
        """Test taking a quiz and verifying activity log recording"""
        self.client.login(email="student@techspire.in", password="StudentPassword123!")
        
        # Auto enroll
        Enrollment.objects.create(user=self.student_user, course=self.course)

        # Take Quiz
        quiz_url = reverse('quizzes:take_quiz', kwargs={'quiz_id': self.quiz.id})
        post_data = {
            f'question_{self.q1.id}': self.choice1.id
        }
        response = self.client.post(quiz_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Congratulations! You Passed!")
        
        # Check QuizAttempt in DB
        attempt = QuizAttempt.objects.filter(user=self.student_user, quiz=self.quiz).first()
        self.assertIsNotNone(attempt)
        self.assertTrue(attempt.passed)
        self.assertEqual(attempt.score, 100)

        # Verify Activity Log was recorded
        logs = ActivityLog.objects.filter(user=self.student_user)
        self.assertTrue(logs.filter(action_type='quiz_submit').exists())

    def test_admin_user_detail_and_telemetry(self):
        """Test 360° individual learner dossier, drop-off telemetry, and CSV export"""
        # Enroll student and record progress
        enrollment = Enrollment.objects.create(user=self.student_user, course=self.course)
        LessonProgress.objects.create(enrollment=enrollment, lesson=self.lesson1, is_completed=True)

        self.client.login(email="admin@techspire.in", password="AdminPassword123!")
        
        # User 360 dossier
        dossier_url = reverse('dashboard:admin_user_detail', kwargs={'user_id': self.student_user.id})
        response = self.client.get(dossier_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex Learner")
        self.assertContains(response, "Python Essentials 1")
        self.assertContains(response, "50%")

        # Course Drop-off Analytics
        course_analytics_url = reverse('dashboard:admin_course_analytics')
        response = self.client.get(course_analytics_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Essentials 1")

        # Lesson Telemetry
        lesson_analytics_url = reverse('dashboard:admin_lesson_analytics', kwargs={'course_id': self.course.id})
        response = self.client.get(lesson_analytics_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1.1 Getting Started with Python")

        # CSV Export
        csv_url = reverse('dashboard:admin_export_csv', kwargs={'report_type': 'users'})
        response = self.client.get(csv_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn("student@techspire.in", response.content.decode('utf-8'))
        self.assertIn("Alex,Learner", response.content.decode('utf-8'))

    def test_no_demo_credentials_on_login_page(self):
        """Ensure no public demo credentials leak onto the login page"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "student@techspire.in")
        self.assertNotContains(response, "admin@techspire.in")
        self.assertNotContains(response, "Demo Credentials")
