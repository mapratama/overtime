from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class Forget(models.Model):

    user = models.ForeignKey('users.User', related_name='forgets')
    new_password = models.CharField(max_length=50, blank=True, null=True)

    STATUS = Choices(
        (1, 'new', 'Baru'),
        (2, 'email_sent', 'Email telah dikirim'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.new)
    has_been_reset = models.BooleanField(default=False)
    created = AutoCreatedField()

    def __unicode__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if self.status == self.STATUS.email_sent and not self.has_been_reset:
            self.user.set_password(self.new_password)
            self.user.save()
            self.has_been_reset = True
        forget = super(Forget, self).save(*args, **kwargs)
        return forget
