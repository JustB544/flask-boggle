from unittest import TestCase
from app import app, boggle_game, root, check_valid_word, end_game
from flask import session
from boggle import Boggle

board = [['Y', 'U', 'Y', 'E', 'L'], ['D', 'S', 'J', 'P', 'X'], ['H', 'J', 'E', 'L', 'Q'], ['C', 'K', 'M', 'L', 'T'], ['Z', 'V', 'H', 'Z', 'T']]


class FlaskTests(TestCase):
    """tests"""

    def test_root(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button id="start">Start!</button>', html)

    def test_check_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = board
            client.get("/")
            resp = client.get('/check', query_string={'word': 'melt'})
            json = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual({'result': 'ok'}, json)

            resp = client.get('/check', query_string={'word': 'pace'})
            json = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual({'result': 'not-on-board'}, json)

            resp = client.get('/check', query_string={'word': 'hjfjdshfh'})
            json = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual({'result': 'not-word'}, json)
    
    def test_game_over(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = board
                change_session["h_score"] = 6
            client.get("/")
            resp = client.post('/gameover', query_string={'score': 5})

            self.assertEqual(resp.status_code, 200)
            with client.session_transaction() as session:
                self.assertEqual(int(session["h_score"]), 6)

            resp = client.post('/gameover', query_string={'score': 7})

            self.assertEqual(resp.status_code, 200)
            with client.session_transaction() as session:
                self.assertEqual(int(session["h_score"]), 7)



    


