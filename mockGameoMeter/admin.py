from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(GameScores)
admin.site.register(GameInfo)
admin.site.register(MetaBars)