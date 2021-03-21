from django.contrib import admin
from .models import Game_Model
from .models import Image_Model
from .models import Developer_Model
from .models import Genre_Model
# Register your models here.
admin.site.register(Game_Model)
admin.site.register(Image_Model)
admin.site.register(Developer_Model)
admin.site.register(Genre_Model)

