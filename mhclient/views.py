# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView 
from .models import Humanoid
import clmh

# Create your views here.
class IndexView(generic.ListView):
	template_name="mhclient/index.html"
	context_object_name='all_humans'
	
	def get_queryset(self):
		return Humanoid.objects.all()

def detail(request, human_id):
	human = get_object_or_404(Humanoid, pk=human_id)
	return render(request, 'mhclient/detail.html', {'human': human})

def deleteobj(request, human_id):
	clmh.delete_obj(human_id)
	server = get_object_or_404(Humanoid, pk=human_id)    
	server.delete()
	return render(request, 'mhclient/index.html')

class HumanoidCreate(CreateView):
	model=Humanoid
	fields=['age','human_name','gender','weight','muscle','height']

class HumanoidEdit(UpdateView):
	model=Humanoid
	fields=['age','human_name','gender','weight','muscle','height']
