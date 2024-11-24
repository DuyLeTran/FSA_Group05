from django.test import TestCase
from user.models import User
from course.models import Course, Enrollment 
from assessments.models import CourseFinalScore 
from achievement.models import PerformanceAnalytics

class PerformanceAnalyticsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.course = Course.objects.create(course_name='Test Course')
        self.enrollment = Enrollment.objects.create(student=self.user, course=self.course)
        self.course_final_score = CourseFinalScore.objects.create(user=self.user, course=self.course, score=95.0)

    def test_create_performance_analytics(self):
        performance = PerformanceAnalytics.objects.get(user=self.user, course=self.course)
        self.assertIsNotNone(performance)
        self.assertEqual(performance.user, self.user)
        self.assertEqual(performance.course, self.course)

    def test_update_performance_analytics(self):
        performance = PerformanceAnalytics.objects.get(user=self.user, course=self.course)
        self.course_final_score.score = 100.0
        self.course_final_score.save()
        performance.refresh_from_db()
        self.assertEqual(performance.score, 100.0)

    def test_delete_performance_analytics(self):
        self.enrollment.delete()
        with self.assertRaises(PerformanceAnalytics.DoesNotExist):
            PerformanceAnalytics.objects.get(user=self.user, course=self.course)

    def test_signal_update_on_course_final_score_save(self):
        self.course_final_score.score = 90.0
        self.course_final_score.save()
        performance = PerformanceAnalytics.objects.get(user=self.user, course=self.course)
        self.assertEqual(performance.score, 90.0)

    def test_signal_update_on_course_save(self):
        self.course.course_name = 'Updated Course'
        self.course.save()
        performance = PerformanceAnalytics.objects.get(user=self.user, course=self.course)
        self.assertEqual(performance.course.course_name, 'Updated Course')

    def test_signal_create_on_enrollment_save(self):
        new_user = User.objects.create(username='newuser')
        new_course = Course.objects.create(course_name='New Course')
        new_enrollment = Enrollment.objects.create(student=new_user, course=new_course)
        performance = PerformanceAnalytics.objects.get(user=new_user, course=new_course)
        self.assertIsNotNone(performance)

    def test_signal_delete_on_enrollment_delete(self):
        new_user = User.objects.create(username='newuser')
        new_course = Course.objects.create(course_name='New Course')
        new_enrollment = Enrollment.objects.create(student=new_user, course=new_course)
        new_enrollment.delete()
        with self.assertRaises(PerformanceAnalytics.DoesNotExist):
            PerformanceAnalytics.objects.get(user=new_user, course=new_course)
from django.test import TestCase
from user.models import User
from .models import AIInsights
from assessments.models import StudentAssessmentAttempt, Assessment, AssessmentType
from course.models import Course, Enrollment
from django.db import IntegrityError

class AIInsightsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(course_name="Test Course", description="Test Course Description")
        self.assessment_type = AssessmentType.objects.create(type_name="Type 1")
        self.assessment = Assessment.objects.create(
        course=self.course,
        created_by=self.user,
        assessment_type=self.assessment_type
    )

    def test_create_aiinsight(self):
        insight = AIInsights.objects.create(
            user=self.user,
            course=self.course,
            insight_text="This is a test insight.",
            insight_type="Positive"
        )

        self.assertEqual(insight.user, self.user)
        self.assertEqual(insight.course, self.course)
        self.assertEqual(insight.insight_text, "This is a test insight.")
        self.assertEqual(insight.insight_type, "Positive")


    def test_update_or_create_on_enrollment_save(self):
        enrollment = Enrollment.objects.create(student=self.user, course=self.course)
        
        insight = AIInsights.objects.get(user=self.user, course=self.course)
        self.assertIsNotNone(insight)
        self.assertEqual(insight.insight_text, None)
        self.assertEqual(insight.insight_type, None)

    def test_delete_on_enrollment_delete(self):
        enrollment = Enrollment.objects.create(student=self.user, course=self.course)
        enrollment.delete()

        with self.assertRaises(AIInsights.DoesNotExist):
            AIInsights.objects.get(user=self.user, course=self.course)



