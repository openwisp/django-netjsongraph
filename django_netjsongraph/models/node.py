from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from uuidfield import UUIDField
from jsonfield import JSONField

from ..base import TimeStampedEditableModel


@python_2_unicode_compatible
class BaseNode(TimeStampedEditableModel):
    """
    NetJSON NetworkGraph Node Object implementation
    """
    id = UUIDField(auto=True, primary_key=True)
    label = models.CharField(max_length=64, blank=True)
    # netjson ID and local_addresses
    addresses = models.CharField(max_length=255, db_index=True)
    properties = JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self._format_addresses()
        super(BaseNode, self).save(*args, **kwargs)

    def _format_addresses(self):
        """
        Ensure address format is correct:
            addr1; addr2; addr3;
        """
        self.addresses = self.addresses.replace(',', ';')\
                                       .replace(' ', '')\
                                       .replace(';', '; ')
        if not self.addresses.endswith(';'):
            self.addresses += ';'

    @property
    def local_addresses(self):
        local_addresses = self.addresses.replace(' ', '').split(';')
        if '' in local_addresses:
            local_addresses.remove('')
        return local_addresses

    @property
    def netjson_id(self):
        if self.addresses:
            return self.local_addresses[0]

    @property
    def name(self):
        if self.label:
            return self.label
        return self.netjson_id
