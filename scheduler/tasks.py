import logging

import requests
from rest_manager.models import (HTTP_METHOD_DELETE, HTTP_METHOD_GET,
                                 HTTP_METHOD_POST, HTTP_METHOD_PUT,
                                 REQUEST_STATUS_COMPLETED,
                                 REQUEST_STATUS_FAILED, REQUEST_STATUS_PENDING,
                                 HttpRequest, HttpResponse)

logger = logging.getLogger(__name__)


def get_method(method):
    """Get the requests function for the method."""
    return {
        HTTP_METHOD_GET: requests.get,
        HTTP_METHOD_POST: requests.post,
        HTTP_METHOD_DELETE: requests.delete,
        HTTP_METHOD_PUT: requests.put,
    }.get(method)


def get_result(request_obj):
    """Make the request and get the result."""
    request_method = get_method(request_obj.method)
    if not request_method:
        logger.error(
            f'Invalid method {request_method} for request {request_obj}'
        )
        request_obj.status = REQUEST_STATUS_FAILED
        return

    kwargs = {}
    if request_obj.payload:
        kwargs['data'] = request_obj.payload
    return request_method(
        request_obj.url,
        headers={
            'content-type': request_obj.content_type,
        },
        **kwargs
    )


def execute_request(request_id):
    """This task executes the given request.

    Args:
        request_id (integer): the ID of the request.
    """
    try:
        request_obj = HttpRequest.objects.get(id=request_id)
    except HttpRequest.DoesNotExist:
        logger.error(
            f'Request with {request_id} does not exist.'
        )
        return

    result = get_result(request_obj)
    result_obj = HttpResponse(
        request=request_obj,
    )
    if result:
        if result.status_code == 200:
            request_obj.status = REQUEST_STATUS_COMPLETED
            result_obj.response = result.json()
        else:
            request_obj.status = REQUEST_STATUS_FAILED
        result_obj.status_code = result.status_code
    else:
        request_obj.status = REQUEST_STATUS_FAILED

    request_obj.save(update_fields=['status'])
    result_obj.save()
