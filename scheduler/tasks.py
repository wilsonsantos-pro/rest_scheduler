import logging

import requests
from rest_manager.models import (HTTP_METHOD_DELETE, HTTP_METHOD_GET,
                                 HTTP_METHOD_POST, HTTP_METHOD_PUT,
                                 REQUEST_STATUS_COMPLETED,
                                 REQUEST_STATUS_FAILED, REQUEST_STATUS_PENDING,
                                 HttpRequest, HttpResponse)

logger = logging.getLogger(__name__)


REQUESTS_METHOD = {
    HTTP_METHOD_GET: requests.get,
    HTTP_METHOD_POST: requests.post,
    HTTP_METHOD_DELETE: requests.delete,
    HTTP_METHOD_PUT: requests.put,
}


def execute_request(request_id):
    """This task executes the given request.

    Args:
        request_id (integer): the ID of the request.
    """
    try:
        request_obj = HttpRequest.objects.get(id=request_id)
    except HttpRequest.DoesNotExist:
        logger.error(f'Request with {request_id}')
        return

    request_method = REQUESTS_METHOD.get(request_obj.method)
    if not request_method:
        logger.error(
            f'Invalid method {request_method} for request {request_obj}'
        )
        request_obj.status = REQUEST_STATUS_FAILED
        return

    if request_obj.payload is not None:
        kwargs = {
            'data': request_obj.payload,
        }
    result = request_method(
        request_obj.url,
        headers={
            'content-type': request_obj.content_type,
        },
        **kwargs
    )

    result_obj = HttpResponse(
        request=request_obj,
        status_code=result.status_code,
    )
    if result.status_code == 200:
        request_obj.status = REQUEST_STATUS_COMPLETED
        result_obj.response = result.json()
    else:
        request_obj.status = REQUEST_STATUS_FAILED

    request_obj.save(update_fields=['status'])
    result_obj.save()
