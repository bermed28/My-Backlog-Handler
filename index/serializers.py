# serializers.py
from rest_framework import serializers
from .models import Game_Model, PlayerAccount, Image_Model, Developer_Model, Genre_Model, Library_Model, Library_Membership

class PlayerAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerAccount
        fields = ('player_name', 'user_name', 'email', 'password')

class GameModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game_Model
        fields = ('game_id','game_title', 'genre_id', 'dev_id', 'platforms','img_id')

class ImageModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image_Model
        fields = ('img_id','img_url')

class DeveloperModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Developer_Model
        fields = ('dev_id','dev_name')

class GenreModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre_Model
        fields = ('genre_id','genre_name')

class LibraryModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library_Model
        fields = ('owner_id','games')

class LibraryMembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library_Membership
        fields = ('game','library','last_played','is_finished')


