from django.contrib import admin

# Register your models here.
from .models import User,receita, Img, Label

admin.site.register(User)
admin.site.register(receita)
admin.site.register(Img)
admin.site.register(Label)