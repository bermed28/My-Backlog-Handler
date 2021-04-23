# serializers.py
from rest_framework import serializers
from .models import Game_Model, PlayerAccount, Image_Model, Library_Model, \
    Library_Membership, Ratings_Model


class PlayerAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerAccount
        fields = ('player_name', 'user_name', 'email', 'password')


class GameModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game_Model
        fields = ('game_id', 'game_title', 'genre_id', 'dev_id', 'platforms', 'img_id')


class ImageModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image_Model
        fields = ('img_id', 'img_url')


class LibraryModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library_Model
        fields = ('owner_id', 'games')


class LibraryMembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library_Membership
        fields = ('game', 'library', 'last_played', 'is_finished', 'forced_to_backlog')


class RatingModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ratings_Model
        fields = ('game', 'user_id', 'overall_rating')
