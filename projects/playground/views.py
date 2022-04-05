from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms
from django.forms import TextInput

from playground import mainsentiment
class NewTask(forms.Form):
    input=forms.CharField(widget=forms.TextInput(attrs={'class':'inputf'}),label='')
        
def input(request):
    return render(request,'index.html',{
        "form":NewTask()
    })
    
def analyze(request):
    if request.method=="POST":
        form=NewTask(request.POST)
        if form.is_valid():
            final="#"+form.cleaned_data["input"]
            data=mainsentiment.find(final)
            final=final.upper()
            return render(request,'result.html',{"data":data,"inp":final})
    return render(request,'index.html',{"form":NewTask()})
        
    
    
