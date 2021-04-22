from django.contrib import admin
from .models import Game_Model, Image_Model, Developer_Model, Genre_Model, Library_Model, Library_Membership, \
    Ratings_Model

# Register your models here.
admin.site.register(Game_Model)
admin.site.register(Image_Model)
admin.site.register(Developer_Model)
admin.site.register(Genre_Model)
admin.site.register(Library_Model)
admin.site.register(Library_Membership)
admin.site.register(Ratings_Model)


