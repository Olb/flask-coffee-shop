import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from src.database.models import setup_db, Drink
from src.api import create_app


class DrinksTestCase(unittest.TestCase):
    """This class represents the drinks test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        project_dir = os.path.dirname(os.path.abspath(__file__))
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "drinks_test"
        self.database_path = "sqlite:///{}".format(
            os.path.join(project_dir, self.database_name))
        setup_db(self.app, self.database_path)

        # Manager and Barista tokens
        self.barista_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYmY1NWJiZTgyMGRmN2EwNDQ5NyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTI3NDUwNCwiZXhwIjoxNTY5MzYwOTA0LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.L1Lr2EbFY5TokQaWh2aAdPyOQRWUnPFj0LIxYXyreq4I6SWr5Bc4dXbFUgJr0tltBj7ufZ2oJEa4VymnIfHryVdUVqKKCm32cbFFqse5ugB_VHQgqHeZsPnLyGIOcncMtC6dXKD0BolweE1d8PL0XkgoJhZjsTN5EM3F-6O2ODmnm0sjeH31ddrwBcV6MkS5MuDTuvYXqO2aWeNT4qwD5hJHXmyGkGQNAxearR8hR8cS4LD4xaB2cnEVHny_DUGHei4an1xhawh9QYZ3Vzb8qCEVGuRYm3VwzDgKKMYVUN5nnqSoGCXSlt398zMCqYV_WGr9N6y7IGkKI_xFiGIk5Q'
        self.manager_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYzMwNGVmMDMyMGRmNGU0YWU5NiIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTI3NjY2OSwiZXhwIjoxNTY5MzYzMDY5LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.cqm-TZaSALiLlm9zeSOHCiasJltDet4-76yDUOIrkM4bH0VZG2-whg5b0fxV-dxyOjKwHtd2fBt-V-hFgzonO6CfpL2G0CsWmfrSTmex5sMJL24YA5ZotX1HsLENntsjza2OCMvBxMiE0HFD8qdekMndweWYxeE5YON-L_0SIYg0RVpZ1WInaEuArh40n-bD84E3fDleczuxslGUSc873rQ6k_2kfI-IxUj-57iezSDmoGEXgUdexi_1sO2eyZ6F3En4Jj0Aka5p5rfps09Bro9uGYIitCFsTh_k7nuHi-KQE80ReZjIONtUNT-G-68tQ2yMyNqtM5Dmorvtb1f5Yw'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # self.new_drink = jsonify()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['drinks'])

    def test_get_drink_details_without_permissions_header(self):
        res = self.client().get('/drinks-detail')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_drink_details_without_invalid_token(self):
        res = self.client().get('/drinks-detail', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUz00NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYmY1NWJiZTgyMGRmN2EwNDQ5NyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTExMTQ2MiwiZXhwIjoxNTY5MTE4NjYyLCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.P-cvwMhqVjTDZqsqC4jrCwQ2uyA5QhcYKjxvnXvwMUNHJUOXMwPu3QQMrSr6BNATP6g6qIBFmH-DBGTQ-W3StJfSFOnlZ267F0-giuHMQgT-3BvohJEwCpK1cmfHEIJf5rOOOuSggvRdD39al2k8S5YczXhQvB2QiNV3VAjWE1kfjfBEB24U47TaKPUqAU614i3vamVh_4rfPVewAQtBW17nB8LjAReiibfj4OlJ-oPXo68OGlAEScz-Wi-HlVyIaeY9W29wvDBqHtcyjDlWNbrOCG0V2G7dscjzWapmGTlOhU29376bJr-UM3doIDLkJ-3Dm7bGGr3j0j2bfOf1RA'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_get_drink_details_with_missing_bearer(self):
        res = self.client().get('/drinks-detail', headers={'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUz00NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYmY1NWJiZTgyMGRmN2EwNDQ5NyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTExMTQ2MiwiZXhwIjoxNTY5MTE4NjYyLCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.P-cvwMhqVjTDZqsqC4jrCwQ2uyA5QhcYKjxvnXvwMUNHJUOXMwPu3QQMrSr6BNATP6g6qIBFmH-DBGTQ-W3StJfSFOnlZ267F0-giuHMQgT-3BvohJEwCpK1cmfHEIJf5rOOOuSggvRdD39al2k8S5YczXhQvB2QiNV3VAjWE1kfjfBEB24U47TaKPUqAU614i3vamVh_4rfPVewAQtBW17nB8LjAReiibfj4OlJ-oPXo68OGlAEScz-Wi-HlVyIaeY9W29wvDBqHtcyjDlWNbrOCG0V2G7dscjzWapmGTlOhU29376bJr-UM3doIDLkJ-3Dm7bGGr3j0j2bfOf1RA'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_drink_details_with_permissions(self):
        res = self.client().get('/drinks-detail',
                                headers={'Authorization': f'Bearer {self.barista_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['drinks'])

    def test_create_drink_without_permissions(self):
        res = self.client().post('/drinks', json={
            'title': 'new drink',
            'recipe': [{"color": "brown", "name": "Brown Syrup", "parts": 1}]
        }, headers={'Authorization': 'Bearer eyJ0eXbiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYmY1NWJiZTgyMGRmN2EwNDQ5NyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTExMTQ2MiwiZXhwIjoxNTY5MTE4NjYyLCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.P-cvwMhqVjTDZqsqC4jrCwQ2uyA5QhcYKjxvnXvwMUNHJUOXMwPu3QQMrSr6BNATP6g6qIBFmH-DBGTQ-W3StJfSFOnlZ267F0-giuHMQgT-3BvohJEwCpK1cmfHEIJf5rOOOuSggvRdD39al2k8S5YczXhQvB2QiNV3VAjWE1kfjfBEB24U47TaKPUqAU614i3vamVh_4rfPVewAQtBW17nB8LjAReiibfj4OlJ-oPXo68OGlAEScz-Wi-HlVyIaeY9W29wvDBqHtcyjDlWNbrOCG0V2G7dscjzWapmGTlOhU29376bJr-UM3doIDLkJ-3Dm7bGGr3j0j2bfOf1RA'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_create_drink_with_permissions(self):
        res = self.client().post('/drinks', json={
            'title': 'new drink',
            'recipe': [{"color": "brown", "name": "Brown Syrup", "parts": 1}]
        }, headers={'Authorization': f'Bearer {self.manager_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_update_drink_without_permissions(self):
        res = self.client().patch('/drinks/1', json={"title": "water6"}, headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYmY1NWJiZTgyMGRmN2EwNDQ5NyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTA3NDQ5NiwiZXhwIjoxNTY5MDgxNjk2LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.ocdR7LEn8XYWYd2Ru__0tWYbBP5yjUhCBbluaRXBhm5ksr3pJCDq5yvwm4kiKLHIAOyouutOJKK2VRCQrxk0CQYkqQQQLWXkAwczcds5e52nVy8vCqAAqosCCLHIl6KdVsFekwGqkYw1PfQgaGcgN4nib7ojCV9ylXdWZ_jYT7-QKf_xY-ZKPbvyMm7jbpUFUbz5GOnOR6bIgWPCQT9xEWUVdlhzFBO3fIl1sPWhPGXAzEJGhmMwh8WyF0pdA5kI1PLJqvZTVSsy0dub9DWiG6X5oC8pNDrfCanPneihxbWBVFUoVlDgkrEbZxxyt-zOg2c58Agh6SyCFdFczanueg'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_drink_with_permissions(self):
        res = self.client().patch('/drinks/1',
                                  json={"title": "water4"}, headers={'Authorization': f'Bearer {self.manager_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['drinks']), 1)

    def test_delete_drink_without_permisions(self):
        res = self.client().delete('/drinks/2', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYmY1NWJiZTgyMGRmN2EwNDQ5NyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTA3NDQ5NiwiZXhwIjoxNTY5MDgxNjk2LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.ocdR7LEn8XYWYd2Ru__0tWYbBP5yjUhCBbluaRXBhm5ksr3pJCDq5yvwm4kiKLHIAOyouutOJKK2VRCQrxk0CQYkqQQQLWXkAwczcds5e52nVy8vCqAAqosCCLHIl6KdVsFekwGqkYw1PfQgaGcgN4nib7ojCV9ylXdWZ_jYT7-QKf_xY-ZKPbvyMm7jbpUFUbz5GOnOR6bIgWPCQT9xEWUVdlhzFBO3fIl1sPWhPGXAzEJGhmMwh8WyF0pdA5kI1PLJqvZTVSsy0dub9DWiG6X5oC8pNDrfCanPneihxbWBVFUoVlDgkrEbZxxyt-zOg2c58Agh6SyCFdFczanueg'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_drink_with_permisions(self):
        res = self.client().delete(
            '/drinks/2', headers={'Authorization': f'Bearer {self.manager_token}'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['delete'], 2)

    def test_delete_drink_with_invalid_drink_id(self):
        res = self.client().delete('/drinks/2000', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYzMwNGVmMDMyMGRmNGU0YWU5NiIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTI3NjY2OSwiZXhwIjoxNTY5MzYzMDY5LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.cqm-TZaSALiLlm9zeSOHCiasJltDet4-76yDUOIrkM4bH0VZG2-whg5b0fxV-dxyOjKwHtd2fBt-V-hFgzonO6CfpL2G0CsWmfrSTmex5sMJL24YA5ZotX1HsLENntsjza2OCMvBxMiE0HFD8qdekMndweWYxeE5YON-L_0SIYg0RVpZ1WInaEuArh40n-bD84E3fDleczuxslGUSc873rQ6k_2kfI-IxUj-57iezSDmoGEXgUdexi_1sO2eyZ6F3En4Jj0Aka5p5rfps09Bro9uGYIitCFsTh_k7nuHi-KQE80ReZjIONtUNT-G-68tQ2yMyNqtM5Dmorvtb1f5Yw'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
