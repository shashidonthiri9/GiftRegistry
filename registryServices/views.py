# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import *
from .Managers import userManager
from .Managers import registryManager
from .Managers import itemManager
from .Managers import constants


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from django.core.cache import cache


def index(request):
    a = {"abc":"24"};

    return  JsonResponse({'foo 1111':'bar'});

def user_list_api(request): 
    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    users = userManager.get_all_users()

    return JsonResponse({"users": users});
   
def user_details_api(request): 
 
    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())
  
    user_id = request.GET['user_id']
    user_details = userManager.get_user(user_id)
   
    return JsonResponse(user_details)

@csrf_exempt
def createtoken_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    #parameters = json.loads(request.body
    username = parameters['username']
    password = parameters['password']
    result = userManager.create_token(username, password)

    return JsonResponse(result)

@csrf_exempt
def get_user_from_token_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    token = request.GET['token']
    user_details = userManager.get_user_from_token(token)
     
    return JsonResponse(user_details)

@csrf_exempt
def delete_token_api(request):
    
    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    token = parameters['token']
    user_id = userManager.delete_token(token)

    return JsonResponse({"user_id": user_id, "logout": True})

@csrf_exempt
def logout_api(request):

     if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

     parameters = json.loads(request.body)
     user_id = parameters['user_id']
     result = userManager.logout(user_id)

     return JsonResponse(result)

@csrf_exempt
def register_user_api(request):   
    #print parameters

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    username = parameters['username']
    email = parameters['email']
    password = parameters['password']

    result = userManager.register_user(username, email, password)   
     
    return JsonResponse(result);

@csrf_exempt
def change_password_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    password = parameters['password']
    user_id = parameters['user_id']

    result = userManager.change_password(user_id, password)

    return JsonResponse(result)

@csrf_exempt
def add_item_inventory_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    result = itemManager.add_item(parameters)

    return JsonResponse(result)

@csrf_exempt
def remove_item_inventory_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    

    result = itemManager.remove_item(parameters)

    return JsonResponse(result)

@csrf_exempt
def add_item_registry_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    registry_id = parameters['registry_id']
    item_id = parameters['item_id']
    user_id = parameters['user_id']
    
    result = registryManager.add_registry_item(user_id, registry_id, item_id)

    return JsonResponse(result)

@csrf_exempt
def remove_item_registry_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    registry_id = parameters['registry_id']
    item_id = parameters['item_id']
    user_id = parameters['user_id']

    result = registryManager.remove_registry_item(user_id, registry_id, item_id)

    return JsonResponse(result)

@csrf_exempt
def create_registry_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    parameters = json.loads(request.body)
    user_id = parameters['user_id']
    public = parameters['public']
    name = parameters['name']
    allowed_users = parameters['allowed_users']

    result = registryManager.create_registry(user_id, name, public, allowed_users)

    return JsonResponse(result)

def get_registry_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    user_id = request.GET['user_id']
    registry_id = request.GET['registry_id']
    result = registryManager.get_registry(registry_id)

    return JsonResponse(result)


def registry_list_api(request):
    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    #print request
    user_id = request.GET['user_id']
    result = registryManager.get_registries(user_id)

    return JsonResponse(result);

@csrf_exempt
def give_access_registry_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())


    parameters = json.loads(request.body)
    user_id = parameters['user_id']
    access_to_user_id = parameters['access_to_user_id']
    registry_id = parameters['registry_id']

    result = registryManager.give_access_registry(user_id, registry_id, access_to_user_id)

    return JsonResponse(result)

@csrf_exempt
def deny_access_registry_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())


    parameters = json.loads(request.body)
    user_id = parameters['user_id']
    deny_to_user_id = parameters['deny_to_user_id']
    registry_id = parameters['registry_id']

    result = registryManager.deny_access_registry(user_id, registry_id, deny_to_user_id)

    return JsonResponse(result)

@csrf_exempt
def assign_item_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())


    parameters = json.loads(request.body)
    user_id = parameters['user_id']
    registry_item_id = parameters['registry_item_id']

    result = registryManager.assign_item(user_id, registry_item_id)

    return JsonResponse(result)

@csrf_exempt
def unassign_item_api(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())


    parameters = json.loads(request.body)
    user_id = parameters['user_id']
    registry_item_id = parameters['registry_item_id']

    result = registryManager.unassign_item(user_id, registry_item_id)

    return JsonResponse(result)

def get_items(request):
   
    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())

    result = itemManager.get_all_items()

    return JsonResponse(result)

@csrf_exempt 
def forgot_password(request):

    if not is_authenticated(request):
        return JsonResponse(not_authenticated_message())


    parameters = json.loads(request.body)
    email_id = parameters['email']
    result = userManager.forgot_password(email_id)
    
    return JsonResponse(result)

def is_authenticated(request):

    if constants.KEY_HTTP_TOKEN not in request.META or request.META[constants.KEY_HTTP_TOKEN] != constants.SECRET_TOKEN:
       return False

    return True

def not_authenticated_message():
    return {
       constants.KEY_STATUS:constants.STATUS_FAILED,
       constants.KEY_MESSAGE: constants.AUTH_ERROR
    }
