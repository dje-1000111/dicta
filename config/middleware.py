import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LogErrorsMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error("Catched Exception: %s", exception, exc_info=True)
        return None
