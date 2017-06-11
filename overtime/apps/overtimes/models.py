from django.db import models
from django.core.validators import MinValueValidator

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class Overtime(models.Model):

    user = models.ForeignKey('users.User', related_name='overtimes')
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    STATUS = Choices(
        (1, 'bid', 'Pengajuan'),
        (2, 'approved_coordinator', 'Disetujui Koodrinator'),
        (3, 'approved_manager', 'Disetujui Manager'),
        (4, 'canceled', 'Batal'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.bid)
    notes_coordinator = models.TextField('Catatan Koordinator', blank=True, null=True)
    notes_manager = models.TextField('Catatan Manager', blank=True, null=True)
    created = AutoCreatedField()

    def __unicode__(self):
        return 'Overtime #%s' % (self.id)
