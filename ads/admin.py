from django.contrib import admin

# Register your models here.
from ads.models import *

admin.site.register(Categories)
admin.site.register(Ads)

