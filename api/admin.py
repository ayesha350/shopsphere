from django.contrib import admin

# Register your models here.


from api.models import *

admin.site.register(MyUser),
admin.site.register(Category)
admin.site.register(Product)
