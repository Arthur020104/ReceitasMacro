
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('registro', views.register, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('receita', views.create_recipe, name='recipe'),
    path('tradutor', views.tradutor, name='tradutor'),
    path('likes', views.likes, name="likes"),
    path("info/<str:content>/<int:id>", views.info, name="info"),
    path('MinhasReceitas', views.MinhasReceitas, name='MinhasReceitas'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)