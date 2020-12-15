from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.core import serializers
import json
import requests





def home(request):
    return render(request, 'python_sample/home.html');


_userIdentifier="";
_password="";
_grantType = "password";
_transactionPin = "";
_orderId = "263626";
_amount = "10";
_languageCode = "en";
_merchantToken = "";

_baseURL = "https://uatgw.nasswallet.com";
_checkoutPageURL = "https://uatcheckout.nasswallet.com/";


def login(request):
    
    gatewayURL = '';

    if request.is_ajax and request.method == "POST":

       endPoint = _baseURL+"/payment/transaction/login";

       headers = {'Content-Type': 'application/json', 'authorization': _merchantToken};

       payload = {"data": {"username": _userIdentifier, "password": _password, "grantType": _grantType} };

       response = requests.post(endPoint, data = json.dumps(payload),  headers = headers);
        
       if(response.status_code == 200 and response.json()['data']):
            gatewayURL =  makeTransaction(response.json()['data']['access_token']);
       else:
            print("login failed, please check and try again");

    return JsonResponse({"url" : gatewayURL})

def makeTransaction(access_token):

    endPoint = _baseURL+"/payment/transaction/initTransaction";
    
    headers = {'Content-Type': 'application/json', 'authorization': f"Bearer {access_token}"};
    
    payload =  {"data": {"userIdentifier": _userIdentifier, "transactionPin": _transactionPin, "orderId": _orderId, "amount": _amount, "languageCode": _languageCode}};
    
    response = requests.post(endPoint, data = json.dumps(payload), headers = headers);

    if(response.status_code == 200 and response.json()['data']['transactionId']):
             
             return f"{_checkoutPageURL}?id={response.json()['data']['transactionId']}&token={response.json()['data']['token']}&userIdentifier={_userIdentifier}";    
             #this is the final url format that the customer will be redirected to.

    else:
             print("transaction failed, please check and try again");

 
