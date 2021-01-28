import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime

def get_data(request):
    return json.loads(request.body.decode("utf-8"))

def type_request(request):
    if request.method != 'POST':
        return True
    else:
        return False

@csrf_exempt
def registration(request):
    response = ''
    if request.method == 'GET':
        if request.user.is_authenticated is False:
            response = json.dumps({'ip': request.META.get('REMOTE_ADDR'), 'time': str(datetime.datetime.now()), 'isAuthorizated': False})
        else:
            response = json.dumps({'ip': request.META.get('REMOTE_ADDR'), 'time': str(datetime.datetime.now()),
                                   'isAuthorizated': True})
    else:
        if request.method == 'POST':
            isSuccess = False
            errorText = ''
            data = get_data(request)
            if User.objects.filter(username=data['login']).exists() is False:
                user = User.objects.create_user(data['login'], data['email'], data['password'])
                user.is_active = True
                user.save()
                isSuccess = True
            else:
                errorText = 'Пользователь с таким логином уже существует'
            response = json.dumps({'isSuccees': isSuccess, 'errorText': errorText})
    return HttpResponse(response)

@csrf_exempt
def login(request):
    response = ''
    if request.method == 'GET':
        if request.user.is_authenticated is False:
            response = json.dumps({'ip':request.META.get('REMOTE_ADDR'), 'time': str(datetime.datetime.now()), 'isAuthorizated': False})
        else:
            response = json.dumps({'ip': request.META.get('REMOTE_ADDR'), 'time': str(datetime.datetime.now()), 'isAuthorizated': True})
    else:
        if request.method == 'POST':
            isSuccess = False
            errorText = ''
            data = get_data(request)
            user = auth.authenticate(username=data['login'], password=data['password'])
            if user is not None:
                isSuccess = True
                auth.login(request, user)
            else:
                errorText = 'Неверный логин или пароль'
            response = json.dumps({'isSuccees': isSuccess, 'errorText': errorText})
    return HttpResponse(response)
