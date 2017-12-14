# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
import thread
import clmh

# Create your models here.
class Humanoid(models.Model):  					
    human_name = models.CharField(default='nabeel',max_length=200)
    gender = models.FloatField(default=1.0)
    age = models.IntegerField(default = 23)
    weight = models.FloatField(default = 0.5)
    muscle = models.FloatField(default = 0.5)
    height = models.IntegerField(default = 180)

    def  get_absolute_url(self):
    	try:
    		return reverse('mhclient:detail', kwargs={"human_id":self.pk})
    	finally :
    		clmh.saviour(self.age, self.gender, self.weight, self.muscle , self.height, self.pk)
    	
    def __str__(self):
        return (self.human_name + ' : ' + str(self.age))
