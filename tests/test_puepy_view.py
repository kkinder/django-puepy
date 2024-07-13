import json
import os
import unittest
from unittest.mock import Mock

from django.http import HttpResponse, Http404


class TestPuePyView(unittest.TestCase):
    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "test_settings"

        from django_puepy.puepy_view import PuePyView

        self.view = PuePyView()

    def test_ajax_method_passes(self):
        def test_fn():
            return "test"

        ajax_method = self.view.ajax(test_fn)
        self.assertEqual(ajax_method(), "test")
        self.assertTrue(hasattr(ajax_method, "_is_ajax"))

    def test_get_context_data_invalid_runtime(self):
        self.view.runtime = "invalid"
        with self.assertRaises(ValueError):
            self.view.get_context_data(some_key="some_value")

    def test_post_method_request_has_no_method(self):
        mock_request = Mock()
        mock_request.body = json.dumps({"args": [], "kwargs": {}})
        with self.assertRaises(Http404):
            self.view.post(mock_request)

    def test_post_method_request_has_non_ajax_method(self):
        def test_fn():
            return "test"

        self.view.test_fn = test_fn
        mock_request = Mock()
        mock_request.body = json.dumps({"method": "test_fn", "args": [], "kwargs": {}})
        with self.assertRaises(Http404):
            self.view.post(mock_request)

    def test_post_method_request_has_ajax_method(self):
        def test_fn():
            return "test"

        self.view.test_fn = self.view.ajax(test_fn)
        mock_request = Mock()
        mock_request.body = json.dumps({"method": "test_fn", "args": [], "kwargs": {}})
        response = self.view.post(mock_request)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.content.decode(), json.dumps("test"))


if __name__ == "__main__":
    unittest.main()
