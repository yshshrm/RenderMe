# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class HumanoidApi(models.Model):
    name = models.CharField(default="test", max_length = false)
    height_cm = models.FloatField(default=180)
    weight_kg = models.FloatField(default=70)
    chest_cm = models.FloatField(default=0)
    waist_cm = models.FloatField(default=0)
    age = models.FloatField(default=0)
    body_fat_distribution = models.FloatField(default=0.5)

    def __str__(self):
        return "{}".format(self.name)

