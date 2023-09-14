from django.db import models


class Website(models.Model):
    url = models.URLField(unique=True)
    seo_diagnosis = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.url
