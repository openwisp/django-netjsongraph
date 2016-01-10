import six

from django.conf import settings

from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError


class TextParser(JSONParser):
    """
    Dummy TextParser accepting any text (used in ReceiveTopologyView)
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            return stream.read().decode(encoding)
        except ValueError as e:  # pragma: nocover
            raise ParseError('text/plain parse error - %s' % six.text_type(e))
