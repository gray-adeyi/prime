from .models import Site
from django.conf import settings
import logging

logger = logging.getLevelName(__name__)


class SiteDataMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # add website data to every request
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response, *args, **kwargs):
        try:
            response.context_data["site"] = Site.objects.all().first()
        except Site.DoesNotExist:
            # Missing site information should not fail silently
            logger.warning(
                "Site models instance of this website has not been created. Some site information may be missing on the responses returned by the server")

        response.context_data["paystack_public_key"] = settings.PAYSTACK_PUBLIC_KEY
        return response
