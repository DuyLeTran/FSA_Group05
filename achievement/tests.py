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



