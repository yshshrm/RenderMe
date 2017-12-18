# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class HumanoidApi(models.Model):
    name = models.CharField(default="Username", max_length = 200)
    key_string = models.CharField(default="", max_length = 255)

    gender = models.FloatField(default=0.5)
    age = models.FloatField(default=25)
    skin_color = models.CharField(default="", max_length = 6)
    body_fat_distribution = models.FloatField(default=0.5)
    height_cm = models.FloatField(default=180)
    weight_kg = models.FloatField(default=60)

    image_path = models.CharField(default="", max_length=255)

    chest_cm = models.FloatField(default=0)
    waist_cm = models.FloatField(default=0)
    
    def __str__(self):
        return "{}".format(self.name)
    
    class Meta:
        ordering = ('name',)

