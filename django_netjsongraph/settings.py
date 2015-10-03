from django.conf import settings

DEFAULT_PARSERS = [
    ('netdiff.OlsrParser', 'OLSRd (txtinfo/jsoninfo)'),
    ('netdiff.BatmanParser', 'batman-advanced (jsondoc/txtinfo)'),
    ('netdiff.BmxParser', 'BMX6 (q6m)'),
    ('netdiff.NetJsonParser', 'NetJSON NetworkGraph'),
    ('netdiff.CnmlParser', 'CNML 1.0'),
]

PARSERS = DEFAULT_PARSERS + getattr(settings, 'NETJSONGRAPH_PARSERS', [])
