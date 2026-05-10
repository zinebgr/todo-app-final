from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('User'))
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    completed = models.BooleanField(_('Completed'), default=False)
    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated at'), auto_now=True)
    due_date = models.DateTimeField(_('Due Date'), blank=True, null=True)
    order = models.IntegerField(_('Order'), default=0)

    class Meta:
        ordering = ['order', '-created']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.title