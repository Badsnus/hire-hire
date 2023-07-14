from http import HTTPStatus
from uuid import uuid4

from django.conf import settings
from django.db.utils import IntegrityError
from requests.api import post
from requests.auth import HTTPBasicAuth

from api_donation.exceptions import (
    CannotFindConfirmationURL,
    YookassaBadRequest,
    YookassaForbidden,
    YookassaInternalError,
    YookassaInvalidCredentials,
    YookassaMethodNotAllowed,
    YookassaNotFound,
    YookassaTooManyRequests,
    YookassaUnsupportedMediaType,
)
from api_donation.models import IdempotenceKey


BAD_STATUSES = {
    HTTPStatus.BAD_REQUEST: YookassaBadRequest,
    HTTPStatus.FORBIDDEN: YookassaForbidden,
    HTTPStatus.INTERNAL_SERVER_ERROR: YookassaInternalError,
    HTTPStatus.METHOD_NOT_ALLOWED: YookassaMethodNotAllowed,
    HTTPStatus.NOT_FOUND: YookassaNotFound,
    HTTPStatus.TOO_MANY_REQUESTS: YookassaTooManyRequests,
    HTTPStatus.UNAUTHORIZED: YookassaInvalidCredentials,
    HTTPStatus.UNSUPPORTED_MEDIA_TYPE: YookassaUnsupportedMediaType,
}


class Payment:

    CONTENT_TYPE = 'application/json'

    def __init__(
            self,
            amount,
            currency=settings.DONATION.default_currency,
            capture=settings.DONATION.is_auto_capture_on,
            description=settings.DONATION.default_description,
    ):
        self.amount = amount
        self.currency = currency
        self.capture = capture
        self.description = description

    @staticmethod
    def _generate_idempotence_key():
        while True:
            try:
                key = uuid4()
                return IdempotenceKey.objects.create(value=key)
            except IntegrityError:
                continue

    def _generate_headers(self):
        return {
            'Idempotence-Key': str(self._generate_idempotence_key()),
            'Content-Type': self.CONTENT_TYPE,
        }

    def _generate_data(self):
        return {
            'amount': {
                'value': self.amount,
                'currency': self.currency,
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': settings.DONATION.return_url,
            },
            'capture': self.capture,
            'description': self.description,
        }

    @staticmethod
    def _validate_request(sent_request):
        if sent_request.status_code in BAD_STATUSES:
            raise BAD_STATUSES[sent_request.status_code]

    def create(self):
        result = post(
            settings.DONATION.api_url,
            json=self._generate_data(),
            headers=self._generate_headers(),
            auth=HTTPBasicAuth(
                settings.DONATION.shop_id,
                settings.DONATION.api_key,
            ),
        )

        self._validate_request(result)

        try:
            return result.json().get('confirmation').get('confirmation_url')
        except AttributeError:
            raise CannotFindConfirmationURL
