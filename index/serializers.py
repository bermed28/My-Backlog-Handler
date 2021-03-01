# serializers.py
from rest_framework import serializers
from .models import PlayerAccount

class PlayerAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerAccount
        fields = ('player_name', 'user_name', 'email', 'password')