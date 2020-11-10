from unittest.mock import patch, PropertyMock
from django.test import TestCase
from mixer.backend.django import mixer

from rest_manager import models as models_rm
from .tasks import get_result, execute_request


def mock_json():
    return ''


class GetResultTest(TestCase):
    """ Tests for tasks.get_result """

    @patch('requests.get')
    def test_get_result(self, get):
        obj = mixer.blend(
            'rest_manager.HttpRequest',
            method=models_rm.HTTP_METHOD_GET,
            status=models_rm.REQUEST_STATUS_PENDING
        )
        get_result(obj)
        self.assertTrue(get.called)


@patch('scheduler.tasks.get_result')
class ExecuteRequestTest(TestCase):
    """ Tests for tasks.execute_request """

    def test_execute_request(self, get_result):
        type(get_result.return_value).status_code = PropertyMock(
            return_value=200)
        type(get_result.return_value).json = PropertyMock(
            return_value=mock_json)
        obj = mixer.blend(
            'rest_manager.HttpRequest',
            status=models_rm.REQUEST_STATUS_PENDING
        )
        execute_request(obj.id)
        obj.refresh_from_db()
        self.assertEqual(obj.status, models_rm.REQUEST_STATUS_COMPLETED)
        self.assertTrue(models_rm.HttpResponse.objects.filter(
            request__id=obj.id, status_code=200
        ).exists())

    def test_execute_request_fail(self, get_result):
        get_result.return_value = None
        obj = mixer.blend(
            'rest_manager.HttpRequest',
            status=models_rm.REQUEST_STATUS_PENDING
        )
        execute_request(obj.id)
        obj.refresh_from_db()
        self.assertEqual(obj.status, models_rm.REQUEST_STATUS_FAILED)
        self.assertFalse(models_rm.HttpResponse.objects.filter(
            request__id=obj.id, status_code=200
        ).exists())

    def test_execute_request_error_status(self, get_result):
        type(get_result.return_value).status_code = PropertyMock(
            return_value=500)
        obj = mixer.blend(
            'rest_manager.HttpRequest',
            status=models_rm.REQUEST_STATUS_PENDING
        )
        execute_request(obj.id)
        obj.refresh_from_db()
        self.assertEqual(obj.status, models_rm.REQUEST_STATUS_FAILED)
        self.assertFalse(models_rm.HttpResponse.objects.filter(
            request__id=obj.id, status_code=200
        ).exists())

    def test_execute_request_no_request(self, get_result):
        obj_id = 1234
        execute_request(obj_id)
        self.assertFalse(models_rm.HttpResponse.objects.filter(
            request__id=obj_id
        ).exists())
