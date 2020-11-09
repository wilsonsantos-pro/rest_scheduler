from unittest.mock import patch, MagicMock
from django.conf import settings
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from mixer.backend.django import mixer

from .admin import HttpRequestAdmin
from .models import REQUEST_STATUS_PENDING, REQUEST_STATUS_COMPLETED
from . import models


class HttpRequestAdminTest(TestCase):

    def test_can_schedule(self):
        obj = mixer.blend('rest_manager.HttpRequest',
                          status=REQUEST_STATUS_COMPLETED)
        result = HttpRequestAdmin.can_schedule(obj, True)
        self.assertTrue(result)

        obj = mixer.blend('rest_manager.HttpRequest',
                          status=REQUEST_STATUS_COMPLETED)
        result = HttpRequestAdmin.can_schedule(obj, False)
        self.assertFalse(result)

        obj = mixer.blend('rest_manager.HttpRequest',
                          status=REQUEST_STATUS_PENDING)
        result = HttpRequestAdmin.can_schedule(obj, False)
        self.assertTrue(result)

    @patch(settings.SCHEDULE_FUNCTION)
    def test_save_model(self, mock_function):
        site = AdminSite()
        request_admin = HttpRequestAdmin(models.HttpResponse, site)
        request = MagicMock()
        form = MagicMock()

        obj = mixer.blend('rest_manager.HttpRequest',
                          status=models.REQUEST_STATUS_PENDING)
        request_admin.save_model(request, obj, form, True)
        self.assertTrue(mock_function.called)

        mock_function.reset_mock()
        obj = mixer.blend('rest_manager.HttpRequest',
                          status=models.REQUEST_STATUS_COMPLETED)
        request_admin.save_model(request, obj, form, False)
        self.assertFalse(mock_function.called)
