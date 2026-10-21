"""Offline tests for lambda_function.py. No AWS account needed: Bedrock and Polly are replaced by fakes.

Run:  python -m unittest backend/test_lambda.py
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import lambda_function as lf  # noqa: E402


def post(question):
    event = {"requestContext": {"http": {"method": "POST"}}, "body": json.dumps({"question": question})}
    resp = lf.lambda_handler(event, None)
    return resp["statusCode"], json.loads(resp["body"])


class BedrockDown(unittest.TestCase):
    """Bedrock throws (for example a quota error): the app must keep working."""

    def setUp(self):
        def boom(_q):
            raise RuntimeError("ThrottlingException: Too many tokens per day")
        self._ask, self._speak = lf.ask_bedrock, lf.synthesize
        lf.ask_bedrock = boom
        lf.synthesize = lambda text: ("QUJD", "Joanna")

    def tearDown(self):
        lf.ask_bedrock, lf.synthesize = self._ask, self._speak

    def test_keyword_clip(self):
        status, body = post("my film is hanging")
        self.assertEqual((status, body["type"], body["topic"], body["source"]), (200, "clip", "buffering", "fallback"))

    def test_hinglish_keyword(self):
        _, body = post("Bachchon ke liye content kaise block karun?")
        self.assertEqual(body["topic"], "parental")

    def test_scripted_answer_is_spoken(self):
        _, body = post("What is the difference between HD and 4K?")
        self.assertEqual(body["type"], "answer")
        self.assertIn("audio", body)

    def test_unrelated_question(self):
        _, body = post("what is the weather")
        self.assertEqual(body["type"], "answer")
        self.assertNotIn("audio", body)


class BedrockUp(unittest.TestCase):
    def setUp(self):
        self._ask, self._speak = lf.ask_bedrock, lf.synthesize
        lf.synthesize = lambda text: ("QUJD", "Joanna")

    def tearDown(self):
        lf.ask_bedrock, lf.synthesize = self._ask, self._speak

    def test_model_picks_tutorial(self):
        lf.ask_bedrock = lambda q: '{"topic": "wifi", "confidence": 0.9, "answer": ""}'
        _, body = post("how do I change my network")
        self.assertEqual((body["type"], body["topic"], body["source"]), ("clip", "wifi", "bedrock"))

    def test_model_writes_answer(self):
        lf.ask_bedrock = lambda q: '{"topic": "none", "confidence": 0.1, "answer": "Press Home, then Settings."}'
        _, body = post("how do I open settings quickly")
        self.assertEqual((body["type"], body["source"]), ("answer", "bedrock"))
        self.assertIn("audio", body)

    def test_low_confidence_is_not_played(self):
        lf.ask_bedrock = lambda q: '{"topic": "wifi", "confidence": 0.2, "answer": "Try Settings."}'
        _, body = post("something vague")
        self.assertEqual(body["type"], "answer")


class Http(unittest.TestCase):
    def test_empty_question(self):
        self.assertEqual(post("   ")[0], 400)

    def test_get_not_allowed(self):
        resp = lf.lambda_handler({"requestContext": {"http": {"method": "GET"}}}, None)
        self.assertEqual(resp["statusCode"], 405)

    def test_options_for_cors(self):
        resp = lf.lambda_handler({"requestContext": {"http": {"method": "OPTIONS"}}}, None)
        self.assertEqual(resp["statusCode"], 204)


if __name__ == "__main__":
    unittest.main()
