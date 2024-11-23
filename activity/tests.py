from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model  # Use this instead of importing User directly
from .models import UserActivityLog
from django.conf import settings
from unittest.mock import patch
from datetime import timedelta

User = get_user_model()  # This ensures compatibility with the custom user model


class ActivityViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.activity_url = reverse('activity:activity_view')
        self.dashboard_url = reverse('activity:activity_dashboard_view')
        self.export_data_url = reverse('activity:export_data')
        self.tag_url = reverse('activity:tag_view')

        # Create some sample activity logs for testing
        for i in range(25):
            UserActivityLog.objects.create(
                user=self.user,
                activity_type='page_visit',
                activity_details=f"Activity {i}",
                activity_timestamp=timezone.now() - timedelta(minutes=i)
            )

    def test_activity_view_renders_correct_template(self):
        response = self.client.get(self.activity_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activity.html')

        def test_activity_view_pagination(self):
            response = self.client.get(self.activity_url, {'page': 1})
            self.assertEqual(response.status_code, 200)
            self.assertIn('activity_logs', response.context)
            self.assertEqual(len(response.context['activity_logs']), 20)  # Assuming pagination limit of 20

    def test_activity_view_search_filter(self):
        UserActivityLog.objects.create(
            user=self.user,
            activity_type='search',
            activity_details="Special search activity",
            activity_timestamp=timezone.now()
        )
        response = self.client.get(self.activity_url, {'search': 'Special'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("Special search activity" in log.activity_details for log in response.context['activity_logs']))

    def test_activity_dashboard_view_post_filter(self):
        response = self.client.post(
            self.dashboard_url,
            {'from_date': '2024-01-01', 'to_date': '2024-12-31'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_activities', response.json())



    def test_fetch_activity_logs_pagination(self):
        fetch_url = reverse('activity:fetch_activity_logs')
        response = self.client.get(fetch_url, {'page': 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('pagination', data)
        self.assertTrue(data['pagination']['has_next'])

    def test_export_data_no_data(self):
        export_url = self.export_data_url + '?search=NonexistentActivity'
        response = self.client.get(export_url)
        self.assertEqual(response.status_code, 404)
        self.assertIn("No data available", response.content.decode())
    
    def test_tag_view_renders_correct_template(self):
        response = self.client.get(self.tag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag.html')
