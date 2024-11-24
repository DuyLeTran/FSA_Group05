from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Assessment, StudentAssessmentAttempt, AssessmentFinalScore, Course, CourseFinalScore,AssessmentType

User = get_user_model()

class AssessmentFinalScoreTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.assessment_type = AssessmentType.objects.create(type_name='Quiz')
        self.course = Course.objects.create(course_name='Test Course')
        self.assessment = Assessment.objects.create(title='Test Assessment',course =self.course, ass_weights=0.5, quiz_weights=0.5, assessment_weights=1.0,created_by=self.user,assessment_type=self.assessment_type)
        
        
        
        self.attempt1 = StudentAssessmentAttempt.objects.create(user=self.user, assessment=self.assessment, score_ass=80, score_quiz=90)
        self.attempt2 = StudentAssessmentAttempt.objects.create(user=self.user, assessment=self.assessment, score_ass=85, score_quiz=95)

    def test_update_score(self):
        final_score = AssessmentFinalScore.objects.get(user=self.user, assessment=self.assessment)
        final_score.update_score()
        self.assertEqual(final_score.final_score_ass, 85 * 0.5)
        self.assertEqual(final_score.final_score_quiz, 95 * 0.5)
        self.assertEqual(final_score.final_score, (85 * 0.5 + 95 * 0.5) * 1.0)

class CourseFinalScoreTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.assessment_type = AssessmentType.objects.create(type_name='Quiz')
        self.course = Course.objects.create(course_name='Test Course')
        self.assessment1 = Assessment.objects.create(title='Test Assessment 1', course=self.course, ass_weights=0.5, quiz_weights=0.5, assessment_weights=0.5,created_by=self.user,assessment_type=self.assessment_type)
        self.assessment2 = Assessment.objects.create(title='Test Assessment 2', course=self.course, ass_weights=0.5, quiz_weights=0.5, assessment_weights=0.5,created_by=self.user,assessment_type=self.assessment_type)
        self.attempt1 = StudentAssessmentAttempt.objects.create(user=self.user, assessment=self.assessment1, score_ass=80, score_quiz=90)
        self.attempt2 = StudentAssessmentAttempt.objects.create(user=self.user, assessment=self.assessment2, score_ass=85, score_quiz=95)

    def test_final_score(self):
        final_score1 = AssessmentFinalScore.objects.get(user=self.user, assessment=self.assessment1)
        final_score1.update_score()
        final_score2 = AssessmentFinalScore.objects.get(user=self.user, assessment=self.assessment2)
        final_score2.update_score()
        course_final_score = CourseFinalScore.objects.get(user=self.user, course=self.course)
        course_final_score.final_score()
        expected_score = final_score1.final_score + final_score2.final_score
        self.assertEqual(course_final_score.score, expected_score)
