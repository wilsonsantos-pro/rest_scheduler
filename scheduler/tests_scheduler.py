import datetime
from unittest.mock import patch
from django.test import TestCase
from mixer.backend.django import mixer

from rest_manager import models as models_rm
from .scheduler import sleep_func, schedule_execution


@patch('scheduler.scheduler.time.sleep')
class SleepFuncTest(TestCase):

    def test_sleep_func_timedelta(self, sleep):
        sleep_func(datetime.timedelta(234))
        self.assertTrue(sleep.called)

    def test_sleep_func_int(self, sleep):
        sleep_func(234)
        self.assertTrue(sleep.called)


class ScheduleExecutionTest(TestCase):

    @patch('scheduler.scheduler.threading.Thread.start')
    def test_schedule_execution(self, thread_start):
        obj = mixer.blend(
            'rest_manager.HttpRequest',
            status=models_rm.REQUEST_STATUS_PENDING
        )
        schedule_execution(obj)
        self.assertTrue(thread_start.called)
