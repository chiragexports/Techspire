from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import User
from apps.courses.models import CourseCategory, Course, Module, Lesson
from apps.quizzes.models import Quiz, Question, Choice, QuizAttempt, UserAnswer
from apps.enrollments.models import Enrollment

class AssessmentAuthenticationAndSubmissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_student@techspire.in',
            email='test_student@techspire.in',
            password='Password123!',
            first_name='Rahul',
            last_name='Sharma',
            role='student'
        )
        self.category = CourseCategory.objects.create(
            name='Python Programming',
            slug='python-programming',
            description='Learn Python'
        )
        self.course = Course.objects.create(
            title='Python Programming: Zero to Pro',
            slug='python-programming-zero-to-pro',
            category=self.category,
            is_published=True,
            is_free=True,
            duration_hours=24.0,
        )
        self.module = Module.objects.create(
            course=self.course,
            title='Python Core Essentials',
            order=1
        )
        self.lesson = Lesson.objects.create(
            module=self.module,
            title='Python Installation & Fundamentals',
            order=1,
            duration_minutes=15,
            lesson_type='article',
            content='Welcome to Python notes.'
        )
        self.quiz = Quiz.objects.create(
            course=self.course,
            title='Python Assessment Quiz',
            pass_percentage=70,
            time_limit_minutes=15,
            max_attempts=5,
            is_published=True
        )
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            prompt='Which keyword defines a function in Python?',
            points=10,
            order=1
        )
        self.c1 = Choice.objects.create(question=self.q1, choice_text='def', is_correct=True)
        self.c2 = Choice.objects.create(question=self.q1, choice_text='function', is_correct=False)

    def test_unauthenticated_user_redirected_to_login(self):
        resp = self.client.get(reverse('quizzes:quiz_detail', kwargs={'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('accounts:login'), resp.url)

    def test_authenticated_user_can_open_assessment_without_login_popup(self):
        login_success = self.client.login(username='test_student@techspire.in', password='Password123!')
        self.assertTrue(login_success)

        # 1. Open Quiz Detail
        resp = self.client.get(reverse('quizzes:quiz_detail', kwargs={'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Python Assessment Quiz')
        self.assertContains(resp, 'Start Quiz Assessment')

        # 2. Open Take Quiz
        resp_take = self.client.get(reverse('quizzes:take_quiz', kwargs={'quiz_id': self.quiz.id}))
        self.assertEqual(resp_take.status_code, 200)
        self.assertContains(resp_take, 'Which keyword defines a function in Python?')
        self.assertContains(resp_take, 'Submit Assessment')

    def test_assessment_submit_flow_calculates_score_and_saves_result(self):
        self.client.login(username='test_student@techspire.in', password='Password123!')

        post_data = {
            f'question_{self.q1.id}': str(self.c1.id)  # Correct answer
        }

        resp_submit = self.client.post(
            reverse('quizzes:take_quiz', kwargs={'quiz_id': self.quiz.id}),
            data=post_data,
            follow=True
        )

        # Should successfully redirect to quiz_result and return 200
        self.assertEqual(resp_submit.status_code, 200)
        self.assertContains(resp_submit, 'Assessment Result')
        self.assertContains(resp_submit, '100')  # 100% score
        self.assertContains(resp_submit, 'Passed')

        # Verify DB records
        attempt = QuizAttempt.objects.filter(user=self.user, quiz=self.quiz).first()
        self.assertIsNotNone(attempt)
        self.assertTrue(attempt.passed)
        self.assertEqual(float(attempt.score), 100.0)

    def test_logout_blocks_assessment(self):
        self.client.login(username='test_student@techspire.in', password='Password123!')
        self.client.logout()

        resp = self.client.get(reverse('quizzes:take_quiz', kwargs={'quiz_id': self.quiz.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('accounts:login'), resp.url)
