# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from bot.models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    pass
