# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from web.forms import FilesForm
from web.models import Files


# Create your views here.
def index(request):
    return render(request, 'index.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = FilesForm(request.POST, request.FILES)
        if form.is_valid():
            if 'fw' in request.FILES:
                fw = request.FILES['fw']
            else:
                return HttpResponse('No find fw')

            fil = Files.objects.up_save(fw=fw)

            return HttpResponse('Success')
        else:
            return HttpResponse('No find fw')
    else:
        return HttpResponse('Failed')
