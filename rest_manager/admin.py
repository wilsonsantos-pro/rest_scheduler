import pydoc

from django.conf import settings
from django.contrib import admin, messages

from .models import REQUEST_STATUS_PENDING, HttpRequest, HttpResponse


@admin.register(HttpRequest)
class HttpRequestAdmin(admin.ModelAdmin):
    list_filter = ('status', 'method', )
    list_display = ('id', 'method', 'url', 'status', 'created', 'modified', )
    list_display_links = ('id', 'url', )

    @staticmethod
    def can_schedule(obj, change):
        """Whether the request can be scheduled.

        :param obj: request object
        :type obj: HttpRequest
        :param form: the form
        :type form: AdminForm
        :param change: whether the form changed
        :type change: bool
        :return: True if the request can be scheduled, False otherwise.
        :type: bool
        """
        return change or obj.status == REQUEST_STATUS_PENDING

    def save_model(self, request, obj, form, change):
        """When the model is saved, call the request scheduler, if
        the conditions are met.

        :param request: the form request to save the model
        :type request: HTTP request
        :param obj: request object
        :type obj: HttpRequest
        :param form: the form
        :type form: AdminForm
        :param change: whether the form changed
        :type change: bool
        """
        super().save_model(request, obj, form, change)
        if self.can_schedule(obj, change):
            # find the scheduler function
            schedule_function = pydoc.locate(settings.SCHEDULE_FUNCTION)
            # schedule the request
            schedule_function(obj)
            messages.add_message(
                request, messages.INFO,
                f'Request scheduled for {obj.eta}'
            )


@admin.register(HttpResponse)
class HttpResponseAdmin(admin.ModelAdmin):
    list_filter = ('status_code', )
    list_display = ('id', 'request', 'status_code', )
    list_display_links = ('id', 'request', )
    readonly_fields = ('status_code', 'response', 'request', )

    def get_queryset(self, request):
        # select_related to reduce repeated queries
        return super().get_queryset(request).select_related('request')
