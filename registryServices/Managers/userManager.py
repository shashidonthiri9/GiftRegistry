from .. import models
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from constants import * 
import smtplib
import random, string

# def add_user():
#     new_user = models.User(name="name", email_id="email_id", password="password", role="role")
#     new_user.save()

#     return  {"user_id": new_user.id}




def get_all_users():

    users = User.objects.all()
    result_users = []
    for user in users: 
        result_users.append({"id":user.id, "username": user.username, "email": user.email, "password": user.password})

    return result_users

def get_user(id):
          
    try:
        user = User.objects.get(id=id)

    except:

        r =  {KEY_STATUS: STATUS_FAILED, 
        KEY_MESSAGE: NOT_FOUND,
        KEY_CODE: NOT_FOUND_CODE
         }

        return r

    return {"id": user.id, "username": user.username, "email": user.email, "password": user.password}

def create_token(username, password):

    user = authenticate(username=username, password=password)

    if not user:
        result = {
        KEY_CODE: FORBIDDEN_CODE, 
        KEY_STATUS: STATUS_FAILED,
        KEY_MESSAGE: AUTH_ERROR
        }

        return result

    token_object = Token.objects.get_or_create(user=user)
    token = token_object[0].key
    result = {"user_id": user.id, "token": token}

    return result

def get_user_from_token(token):

    try:
        token_object = Token.objects.get(key=token)
 
    except:
        result = {
        KEY_CODE: NOT_FOUND_CODE, 
        KEY_STATUS: STATUS_FAILED,
        KEY_MESSAGE: NOT_FOUND
        }

        return result

    user_id = token_object.user_id

    user_details = get_user(user_id)

    return user_details

def delete_token(token):

    token_object = Token.objects.get(key=token)
    user_id = token_object.user_id

    user = User.objects.get(id=id)   
    user.auth_token.delete()

    return user_id

def logout(user_id):

    try:
        user = User.objects.get(id=user_id)   
    except:
        result = {
        KEY_CODE: NOT_FOUND_CODE, 
        KEY_STATUS: STATUS_FAILED,
        KEY_MESSAGE: NOT_FOUND
        }

        return result

    try:
       user.auth_token.delete()
    except:
       a = 10
    finally:
        return {KEY_STATUS: STATUS_SUCCESS}
        #return {"user_id": user_id}


def change_password(user_id, password):

    try:

        u = User.objects.get(id=user_id)
        u.set_password(password)
        u.save()

    except:
        return {KEY_STATUS: STATUS_FAILED}

    return {KEY_STATUS: STATUS_SUCCESS}
    

def register_user(username, email, password):

    try:
        user = User.objects.create_user(username, email, password)
    except:
        result = { 
           KEY_STATUS: STATUS_FAILED,
           KEY_MESSAGE: USERACCOUNT_EXISTS
        }
        return result

    return {KEY_STATUS: STATUS_SUCCESS, 'user_id': user.id}

def forgot_password(email):

    try: 
        user = User.objects.filter(email=email)
        new_password = randomword(5)
        

        change_password(user[0].id, new_password)

        msg = 'Hi. Your new password is '+ new_password

        server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('giftaway.wpl@gmail.com','giftaway123')
        server.sendmail('giftaway.wpl@gmail.com',email,msg)
        server.close()

    except Exception as e: 

        print e
        result = { 
           KEY_STATUS: STATUS_FAILED,
           KEY_MESSAGE: SOMETHING_WENT_WRONG
        }
        return result

    return {KEY_STATUS: STATUS_SUCCESS, 'user_id': user[0].id}

def randomword(length):

    return ''.join(random.choice(string.lowercase) for i in range(length))

#def randomword(length):

#    return ''.join(random.choice(string.lowercase) for i in range(length))