import datetime
from unittest.mock import patch
from django.test import TestCase

from .scheduler import sleep_func


@patch('scheduler.scheduler.time.sleep')
class SleepFuncTest(TestCase):

    def test_sleep_func_timedelta(self, sleep):
        sleep_func(datetime.timedelta(234))
        self.assertTrue(sleep.called)

    def test_sleep_func_int(self, sleep):
        sleep_func(234)
        self.assertTrue(sleep.called)
