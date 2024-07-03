from django.contrib import admin
from .models import Location, Item, User

admin.site.register(Item)
admin.site.register(Location)
admin.site.register(User)
