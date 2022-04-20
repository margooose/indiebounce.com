from django.contrib import admin
from .models import Game, GameSegment, UpdateLog
# Register your models here.
admin.site.register(Game)
admin.site.register(GameSegment)
admin.site.register(UpdateLog)
