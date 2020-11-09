import logging
import sched
import threading
import time

from django.utils import timezone

from .tasks import execute_request

logger = logging.getLogger(__name__)


def sleep_func(timedelta):
    """Sleep function to be used by the scheduler.

    :param timedelta: amount of time to sleep.
    :type timedelta: datetime.timedelta or int
    """
    if isinstance(timedelta, int):
        time.sleep(timedelta)
    else:
        time.sleep(timedelta.seconds)


def schedule_execution(request_obj):
    """Schedule execution.

    It creates the schedule event object and the starts the running thread.

    If the ETA is less than or equal than the current time, the request will
    be executed immediately.

    :param request_obj: HTTP request object
    :type request_obj: models.HttpRequest
    """
    scheduler = sched.scheduler(timezone.now, sleep_func)
    scheduler.enterabs(
        request_obj.eta, 1, execute_request,
        argument=(request_obj.id, )
    )
    thread = threading.Thread(target=scheduler.run, args=(scheduler, ))
    thread.start()
