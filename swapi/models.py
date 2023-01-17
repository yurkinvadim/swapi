from django.db import models
from django.urls import reverse
import petl as etl

from config.settings import MEDIA_ROOT


class Collection(models.Model):
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('collection-detail', args=[str(self.id)])

    @property
    def table(self):
        return etl.fromcsv(f'{MEDIA_ROOT}/{self.filename}')

    class Meta:
        ordering = ['-created_at']
