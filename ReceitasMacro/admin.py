from django.contrib import admin

# Register your models here.
from .models import User,receita, Img, Label

class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'name','sender','public')
    list_display_links = ('id', 'name')
    search_fields = ['name']
    list_editable= ['public']
    list_filter= ['label']
    list_per_page= 5
class ListandoImgs(admin.ModelAdmin):
    list_display = ('id', 'img')
    list_display_links = ('id', 'img')
    search_fields = ['img']
class ListandoUsers(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')
    search_fields = ['username']
admin.site.register(User,ListandoUsers)
admin.site.register(receita,ListandoReceitas)
admin.site.register(Img,ListandoImgs)
admin.site.register(Label)