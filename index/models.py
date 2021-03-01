from django.db import models

# Create your models here.
class PlayerAccount(models.Model):
    player_name = models.CharField(max_length=128)
    user_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)


    def __str__(self):
        return self.user_name