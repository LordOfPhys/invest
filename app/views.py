import json

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app.models import *
import datetime

def get_data(request):
    return json.loads(request.body.decode("utf-8"))

def type_request(request):
    if request.method != 'POST':
        return True
    else:
        return False

@csrf_exempt
def get_profile(request):
    if request.headers.get('Authorization'):
        token = request.headers.get('Authorization').split(' ')[1]
        up = UserProfile.objects.get(user=Token.objects.get(key=token).user)
        response = json.dumps({'first_name': up.get_first_name(), 'last_name': up.get_last_name(), 'email': up.get_email()})
    else:
        response = json.dumps({'errorText': 'No token'})
    return HttpResponse(response)

@csrf_exempt
def change_profile(request):
    if request.headers.get('Authorization') and request.method == 'POST':
        token = request.headers.get('Authorization').split(' ')[1]
        up = UserProfile.objects.get(user=Token.objects.get(key=token).user)
        data = get_data(request)
        up.set_first_name(data['first_name'])
        up.set_last_name(data['last_name'])
        up.set_email(data['email'])
        response = json.dumps({'issuccess': True})
    else:
        response = json.dumps({'errorText': 'No token'})
    return HttpResponse(response)


@csrf_exempt
def main_team(request):
    response = []
    for_response = TeamProject.objects.all()
    for i in for_response:
        item = {'label': i.get_label(), 'money_amount': i.get_money_amount(),
                'description': i.get_description(), 'file_url': i.get_file().url,
                'item_id': i.get_item_id()}
        response.append(item)
    return HttpResponse(json.dumps({'response': response}))

@csrf_exempt
def main_invest(request):
    response = []
    for_response = InvestProject.objects.all()
    for i in for_response:
        item = {'label': i.get_label(), 'money_amount': i.get_money_amount(),
            'description': i.get_description(), 'file_url': i.get_file().url,
            'item_id': i.get_item_id()}
        response.append(item)
    return HttpResponse(json.dumps({'response': response}))

@csrf_exempt
def get_invest_item(request):
    data = get_data(request)
    item = InvestProject.objects.get(item_id=data['id'])
    return HttpResponse(json.dumps({'label': item.get_label(), 'description': item.get_description(),
        'money_amount': item.get_money_amount(), 'file_url': item.get_file().url}))

@csrf_exempt
def get_team_item(request):
    data = get_data(request)
    item = TeamProject.objects.get(item_id=data['id'])
    return HttpResponse(json.dumps({'label': item.get_label(), 'description': item.get_description(),
        'money_amount': item.get_money_amount(), 'file_url': item.get_file().url}))


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
                Token.objects.get_or_create(user=user)
                token = user.auth_token.key
                auth.login(request, user)
            else:
                token = 'No token'
                errorText = 'Неверный логин или пароль'
            response = json.dumps({'isSuccees': isSuccess, 'errorText': errorText, 'token': token})
    return HttpResponse(response)

@csrf_exempt
def logout(request):
    try:
        user = Token.objects.get(key=request.headers.get('Authorization').split(' ')[1]).user
        user.auth_token.delete()
        response = json.dumps({'isSuccess': True})
    except (AttributeError, ObjectDoesNotExist):
        response = json.dumps({'errorText': 'Error. Try later.'})
    return HttpResponse(response)
