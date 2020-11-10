import django.utils
from django.db import models
from django_extensions.db.models import TimeStampedModel

HTTP_METHOD_GET = 'GET'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_DELETE = 'DELETE'
HTTP_METHOD_PUT = 'PUT'

HTTP_METHOD_ALL = [
    HTTP_METHOD_GET,
    HTTP_METHOD_POST,
    HTTP_METHOD_DELETE,
    HTTP_METHOD_PUT,
]

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_ALL = [
    CONTENT_TYPE_JSON
]

REQUEST_STATUS_PENDING = 'P'
REQUEST_STATUS_FAILED = 'F'
REQUEST_STATUS_COMPLETED = 'C'

REQUEST_STATUS_CHOICES = (
    (REQUEST_STATUS_PENDING, 'Pending'),
    (REQUEST_STATUS_FAILED, 'Failed'),
    (REQUEST_STATUS_COMPLETED, 'Completed'),
)


class HttpRequest(TimeStampedModel):
    method = models.CharField(
        blank=False,
        null=False,
        default=HTTP_METHOD_GET,
        max_length=10,
        choices=zip(HTTP_METHOD_ALL, HTTP_METHOD_ALL),
        help_text='HTTP method for the request'
    )
    url = models.URLField(
        blank=False,
        null=False,
        help_text='URL for the request',
    )
    content_type = models.CharField(
        default=CONTENT_TYPE_JSON,
        max_length=255,
        choices=zip(CONTENT_TYPE_ALL, CONTENT_TYPE_ALL)
    )
    payload = models.TextField(
        blank=True,
        null=True,
        max_length=2048,
        help_text='Request body. Must be compatible with content type'
    )
    eta = models.DateTimeField(
        default=django.utils.timezone.now,
        help_text='When the request is expected to be run.'
    )
    status = models.CharField(
        max_length=1,
        choices=REQUEST_STATUS_CHOICES,
        default=REQUEST_STATUS_PENDING,
        editable=False,
        help_text='Request status',
    )

    def __str__(self):
        return f'{self.id} | {self.method} {self.url}'


class HttpResponse(TimeStampedModel):
    request = models.ForeignKey(
        HttpRequest,
        on_delete=models.CASCADE,
        editable=False,
    )
    status_code = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
        help_text='HTTP response status. Eg, 200 or 404'
    )
    response = models.CharField(
        max_length=2048,
        null=True,
        editable=False,
    )

    def __str__(self):
        return f'{self.id} | {self.request} - {self.status_code}'
