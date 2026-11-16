"""
Unit and integration test script for SignEase
Verifies database, routes, model loading, and API responses.
"""
import unittest
import json
import base64
import numpy as np
import cv2
from app import app
from models import init_db, get_or_create_daily_assignment, get_progress_summary, get_lessons

class TestSignEase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        init_db()

    def test_database_lessons(self):
        lessons = get_lessons()
        self.assertGreaterEqual(len(lessons), 10, "Expected at least 10 lessons in database")

    def test_daily_assignment_rotation(self):
        assignment, questions = get_or_create_daily_assignment('2026-11-16')
        self.assertEqual(len(questions), 5, "Expected exactly 5 questions for daily assignment")
        
        # Test next day rotation gives valid set
        assignment2, questions2 = get_or_create_daily_assignment('2026-11-17')
        self.assertEqual(len(questions2), 5)

    def test_routes_200_ok(self):
        routes = ['/', '/learn', '/learn?category=words', '/lesson/HELLO', '/assignment', '/progress']
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")

    def test_model_status_api(self):
        response = self.client.get('/api/model-status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'ready')
        self.assertIn('HELLO', data.get('classes', []))

    def test_recognize_api_no_hand(self):
        # Create blank 100x100 black image (no hand)
        blank = np.zeros((100, 100, 3), dtype=np.uint8)
        _, buffer = cv2.imencode('.jpg', blank)
        b64 = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')

        payload = {
            'image': b64,
            'assignment_id': 1,
            'question_num': 1,
            'expected_sign': 'HELLO'
        }
        response = self.client.post('/api/recognize', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data.get('hand_detected'))
        self.assertIn("Hand not detected", data.get('message', ''))

if __name__ == '__main__':
    unittest.main()
