import re
from django.http import response
from requests.api import request
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from application.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from application.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework import status
from datetime import date
import json
import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions
import http.client
# authenticate: will check if the user exist
from django.contrib.auth import authenticate
# api_settings: will help generating the token
from rest_framework_jwt.settings import api_settings
# Create your views here.

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from .serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        print(password)
        if (not email) or (not email[0]):
                return Response("Email is missing.", status=status.HTTP_400_BAD_REQUEST)
        elif (not password) or (not password[0]):
                return Response("Password is missing.", status=status.HTTP_400_BAD_REQUEST)
        # password = make_password(password)
        # try:
        # print(User.objects.filter(email=email))
        # if User.objects.filter(email=email).exists():
        #     print("in")
        else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer = self.get_serializer(data=request.data)
                # print(serializer)
                # print("...", request.data)
                password = request.data['password']
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                return Response({'JWT Authentication Token': token.key, 'User id': token.user_id}, status=status.HTTP_200_OK)
            except:
                return Response({'Error': "Email and Password Combination is Wrong"}, status.HTTP_401_UNAUTHORIZED)
        # else:
        #     return Response("Above fields are missing.",status=status.HTTP_400_BAD_REQUEST)
        # except Exception as error:
        #         return Response({'error': error}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        


obtain_token = ObtainAuthToken.as_view()


conn = http.client.HTTPConnection("2factor.in")

def index(request):
    return render(request, 'index.html')


@csrf_exempt
# @renderer_classes((JSONRenderer))
def register(request):
    form = UserRegisterForm(request.POST)
    print("asdflksaajfls", form.data)
    email = form.data.get('email')
    print(email)
    password = form.data.get('password')
    name = form.data.get('name')
    if (not email) or (not email[0]):
        print("lol")
        return JsonResponse({'email': 'field is missing.'}, status=status.HTTP_400_BAD_REQUEST)
    elif (not name) or (not name[0]):
        return JsonResponse({'name': 'field is missing.'}, status=status.HTTP_400_BAD_REQUEST)
    elif (not password) or (not password[0]):
        return JsonResponse({'password': 'field is missing.'}, status=status.HTTP_400_BAD_REQUEST)
    # print(request.POST)
    # print(form)
    elif form.is_valid():
        form.save()
        sign_up = form.save(commit = False)
        sign_up.password = make_password(form.cleaned_data['password'])
        sign_up.status = 1
        sign_up.save()
        token = Token.objects.all()
        # print(token)
        tk = token[len(token) - 1]
        print("Token: ", tk.key)
        # request['token'] = token
        user = User.objects.all()

        usr = user[len(user) - 1]
        print("User_id: ", usr.id)
        return JsonResponse({'JWT Authentication Token': tk.key, 'User id': usr.id}, status=status.HTTP_200_OK)
    else :
        # return JsonResponse({"Password is too similar"})
        print(form.errors.as_json())
        # return JsonResponse({"Password is too similar"})
        # return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR ,data=form.errors.as_json())
        # print("pass is too similar")
        # return JsonResponse({"Password is too similar"})

@api_view(["GET"])
def AdvisorGetList(request , user):
    if request.method == "GET":

        datad = Advisor.objects.filter()
        dataJson = advisorgetSerializers(datad, many=True)
        # return Response(dataJson.data)
        # dd = dataJson.data[:]
        return Response(dataJson.data)

@api_view(["POST"])
def AdvisorPostList(request):
    if request.method == "POST":
        serializer = advisorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def BookacallList(request, user, Advisor_id):
    if request.method == "POST":
        data = request.data
        data['user'] = user
        data['Advisor_id'] = Advisor_id
        serializer = bookacallSerializers(data=data)
        print(".......", serializer)
        print("... ", type(request.data))
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def callGetList(request, user):
    if request.method == "GET":

        datad = bookacall.objects.filter(user=user)
        datad1 = Advisor.objects.filter()
        data1Json = advisorgetSerializers(datad1, many=True)
        dataJson = bookacallgetSerializers(datad, many=True)
        print(data1Json.data)
        print(dataJson.data)
        # return Response(dataJson.data)
        # dd = dataJson.data[:]
        data = []
        for i in data1Json.data:
            # already_added = False
            for j in dataJson.data:
                if i['Advisor_id']==j['Advisor_id']:
                    data.append({**i, **j})
                    # already_added = True
            # if not already_added:
                # data.append(i)
        return Response(data, status=status.HTTP_200_OK)
    
