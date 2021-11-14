from re import T
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from application.models import *
from application.serializers import *


class userSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  '__all__'

class advisorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = '__all__'

class bookacallSerializers(serializers.ModelSerializer):
    class Meta:
        model = bookacall
        fields = '__all__'

class bookacallgetSerializers(serializers.ModelSerializer):
    class Meta:
        model = bookacall
        fields = ['Booking_id', 'Booking_time','Advisor_id',]

class advisorgetSerializers(serializers.ModelSerializer):
    data = bookacall.objects.filter()
    # tracks = bookacallgetSerializers(data, many = True)
    
    class Meta:
        model = Advisor
        fields = ['Advisor_Name', 'Advisor_Photo_Url', 'Advisor_id',]


# class bothSerializers(serializers.Serializer):
#     tata = bookacallgetSerializers(many=True)
#     tat = advisorgetSerializers(many=True)

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
