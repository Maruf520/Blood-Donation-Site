from django.shortcuts import render
from django.http import HttpResponse 

def dashboard(request):

    # return render(request,'Dashboard/base.html')

    return render(request, 'dashboard/base.html')