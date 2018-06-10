from rest_framework import serializers
from models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
    	model = User
    	fields = ('id', 'username', 'email')

class RegistrySerializer(serializers.ModelSerializer) :

    class Meta:
        model = Registry
        fields = ('owner_id', 'public')


class RegistryItemSerializer(serializers.ModelSerializer):

	class Meta:
        model = RegistryItem
        fields = ('item_id', 'assigned_to')
