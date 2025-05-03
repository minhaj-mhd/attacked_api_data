from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import now, timedelta
from .models import Attack, Location

class AttackAPITestCase(APITestCase):

    def setUp(self):
        """Create sample data for tests"""
        # Locations
        loc_us = Location(latitude=37.7749, longitude=-122.4194, country="USA")
        loc_cn = Location(latitude=39.9042, longitude=116.4074, country="China")

        # Create some attacks
        Attack(
            source_location=loc_us,
            destination_location=loc_cn,
            attack_type="DDoS",
            severity=5,
            timestamp=now() - timedelta(days=1),
            additional_details={"description": "Distributed denial of service"}
        ).save()

        Attack(
            source_location=loc_cn,
            destination_location=loc_us,
            attack_type="Phishing",
            severity=7,
            timestamp=now(),
            additional_details={"description": "Email phishing campaign"}
        ).save()
    def tearDown(self):
        Attack.drop_collection()

    def test_list_attacks(self):
        """Test listing attacks with pagination"""
        response = self.client.get('/api/attacks/', {'page': 1, 'page_size': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_attack_type(self):
        """Test filtering attacks by type"""
        response = self.client.get('/api/attacks/', {'attack_type': 'DDoS'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['attack_type'], 'DDoS')

    def test_filter_by_severity(self):
        """Test filtering attacks by severity"""
        response = self.client.get('/api/attacks/', {'severity': 7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_date_range(self):
        """Test filtering by start and end date"""
        today = now().isoformat()
        yesterday = (now() - timedelta(days=2)).isoformat()
        response = self.client.get('/api/attacks/', {'start_date': yesterday, 'end_date': today})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_invalid_date_format(self):
        """Test invalid date format handling"""
        response = self.client.get('/api/attacks/', {'start_date': 'invalid', 'end_date': 'also-invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recent_attacks(self):
        """Test fetching recent attacks"""
        response = self.client.get('/api/attacks/recent/', {'limit': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_attack_statistics(self):
        """Test statistics aggregation by country"""
        response = self.client.get('/api/attacks/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('USA', response.data)
        self.assertIn('China', response.data)

    def test_visualization_data(self):
        """Test GeoJSON visualization data structure"""
        response = self.client.get('/api/attacks/visualization-data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], 'FeatureCollection')
        self.assertIsInstance(response.data['features'], list)
        self.assertGreater(len(response.data['features']), 0)
