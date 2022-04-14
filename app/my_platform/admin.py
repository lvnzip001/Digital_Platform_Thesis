from django.contrib import admin

from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User_Info)
admin.site.register(Embed_Ownership_Image)
admin.site.register(Embed_Enforcement_Image)
admin.site.register(Embedded_Files)