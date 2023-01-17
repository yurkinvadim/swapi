from django.db import models
from django.urls import reverse


class Collection(models.Model):
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('collection-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_at']
