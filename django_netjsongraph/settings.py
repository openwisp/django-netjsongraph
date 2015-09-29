from django.conf import settings
from datetime import timedelta

DEFAULT_PARSERS = [
    ('netdiff.OlsrParser', 'OLSRd (txtinfo/jsoninfo)'),
    ('netdiff.BatmanParser', 'batman-advanced (jsondoc/txtinfo)'),
    ('netdiff.BmxParser', 'BMX6 (q6m)'),
    ('netdiff.NetJsonParser', 'NetJSON NetworkGraph'),
    ('netdiff.CnmlParser', 'CNML 1.0'),
]

PARSERS = DEFAULT_PARSERS + getattr(settings, 'NODESHOT_NETDIFF_PARSERS', [])
TOPOLOGY_UPDATE_INTERVAL = getattr(settings, 'NODESHOT_TOPOLOGY_UPDATE_INTERVAL', 3)
