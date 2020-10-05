from django.contrib import admin
from models import *
from django.utils.translation import ugettext as _
# Register your models here.

class adminPark(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Park,adminPark)

