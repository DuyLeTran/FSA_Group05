from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from ..forms import *
from .modules.export_assistant import ExportJSON
from .modules.json_handler import get_index_from_id
import json

def json_upload(request):
    if request.method == 'POST':
        json_form = JSONForm(request.POST, request.FILES)
        if json_form.is_valid():
            uploaded_file = request.FILES['json_file']
            file_content = uploaded_file.read().decode('utf-8')
            json_data = json.loads(file_content)
            request.session['json_for_modification'] = json_data

            return redirect('quiz_bank:json_modification')
    else:
        json_form = JSONForm()
    return render(request, 'json_upload.html', context={'form': json_form})

def json_modification(request):
    if 'json_for_modification' in request.session:
        json_data = request.session['json_for_modification']
    else:
        return HttpResponseBadRequest('Bad Request: No JSON data received in HttpRequest.')

    if request.method == 'POST':
        if 'json' in request.POST:
            json_form = JSONForm(request.POST, request.FILES)
            if json_form.is_valid():
                uploaded_file = request.FILES['json_file']
                file_content = uploaded_file.read().decode('utf-8')
                json_data = json.loads(file_content)
                request.session['json_for_modification'] = json_data

            return redirect('quiz_bank:json_modification')
        elif 'download' in request.POST:
            return ExportJSON(json_data).export(file_name='questions')
    else:
        json_form = JSONForm()
    return render(request, 'json_modification.html', context={'form': json_form, 'question_list': json_data})

def json_delete_question(request, question_id):
    if 'json_for_modification' in request.session:
        request.session['json_for_modification'].pop(get_index_from_id(request.session['json_for_modification'], id=question_id))
    else:
        return HttpResponseBadRequest('Bad Request: No JSON data received in HttpRequest.')
    return redirect('quiz_bank:json_modification')

def json_edit_question(request, question_id):
    if 'json_for_modification' in request.session:
        index = get_index_from_id(request.session['json_for_modification'], id=question_id)
    else:
        return HttpResponseBadRequest('Bad Request: No JSON data received in HttpRequest.')

    

    if request.method == 'POST':
        return redirect('quiz_bank:json_modification')
    

    


