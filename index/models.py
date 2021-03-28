from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class PlayerAccount(models.Model):
    player_name = models.CharField(max_length=128)
    user_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)


    def __str__(self):
        return self.user_name

class Genre_Model(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=128)

class Developer_Model(models.Model):
    dev_id = models.IntegerField(primary_key=True)
    dev_name = models.CharField(max_length=128)

class Image_Model(models.Model):
    img_id = models.IntegerField(primary_key=True)
    img_url = models.URLField(max_length=200)

class Game_Model(models.Model):
    game_id = models.IntegerField(primary_key=True)
    game_title = models.CharField(max_length=128)

    genre_id = models.ForeignKey(Genre_Model, on_delete=models.CASCADE)
    dev_id = models.ForeignKey(Developer_Model, on_delete=models.CASCADE)
    platforms = JSONField()
    img_id = models.ForeignKey(Image_Model, on_delete=models.CASCADE)


