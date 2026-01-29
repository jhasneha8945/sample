from django.db import models
import json
import pandas as pd

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    csv_data = models.TextField()  # JSON-serialized DF
    summary = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Keep only last 5 datasets
        if Dataset.objects.count() >= 5:
            Dataset.objects.last().delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
