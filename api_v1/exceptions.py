from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class BadUrlValueException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Bad value in url"
    default_code = "bad_url_value"
