from django.contrib import admin

# Register your models here.
from .models import User,receita, Img

admin.site.register(User)
admin.site.register(receita)
admin.site.register(Img)