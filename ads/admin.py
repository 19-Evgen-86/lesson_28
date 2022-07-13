from django.contrib import admin

# Register your models here.
from ads.models import *

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Ads)
admin.site.register(Locations)
