# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Prediction(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='predictions/', blank=True, null=True)

    def __str__(self):
        return self.text[:50]