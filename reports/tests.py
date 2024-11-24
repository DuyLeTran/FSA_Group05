from django.test import TestCase
from django.urls import reverse
from user.models import User
from module_group.models import ModuleGroup, Module
from activity.models import UserActivityLog
from course.models import Course, Session
from datetime import timedelta
from django.utils.timezone import now


class RiskPredictionReportTest(TestCase):
    
    def setUp(self):
        # Create test data for the courses, users, and activity logs
        self.user = User.objects.create_user(username='testuser', password='password')
        self.course = Course.objects.create(course_name='Test Course')
        self.session = Session.objects.create(course=self.course, name='Test Session', order = 1)
        
        # Create Activity Logs
        UserActivityLog.objects.create(user=self.user, course=self.course, activity_details='')
        UserActivityLog.objects.create(user=self.user, course=self.course, activity_details='Test activity for Test Course')

    def test_risk_prediction_report_view(self):
        # Get the URL for the view
        url = reverse('risk_prediction_report')

        # Send a GET request to the view
        response = self.client.get(url)

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the context contains the expected keys
        self.assertIn('evaluation_report', response.context)
        self.assertIn('labels', response.context)
        self.assertIn('data', response.context)
        self.assertIn('paginator', response.context)
        self.assertIn('paginated_data', response.context)

        # Check that the correct course data appears in the evaluation report
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'testuser')
        self.assertContains(response, '2')  # 2 activities logged for the user

    def test_pagination(self):
        # Create more data to ensure pagination is tested
        for i in range(10):
            UserActivityLog.objects.create(user=self.user, course=self.course, activity_details=f'Test activity {i} for Test Course')

        url = reverse('risk_prediction_report')
        response = self.client.get(url + '?page=2')

        # Check that pagination is working (i.e., only 8 items per page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Next &raquo;')  # Ensure that the next page link is present

    def test_filtering_by_course(self):
        # Test that the filtering works by checking a different course
        other_course = Course.objects.create(course_name='Another Course')
        UserActivityLog.objects.create(user=self.user, course=other_course, activity_details='Test activity for Another Course')

        url = reverse('risk_prediction_report')
        response = self.client.get(url)

        # Check that both courses are included in the report
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'Another Course')

