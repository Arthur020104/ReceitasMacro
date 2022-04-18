from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User, receita, Img
import json
from googletrans import Translator
from datetime import datetime

def index(request):
    minute = int(datetime.now().strftime("%M"))
    if minute % 5 == 0:
        receitas = receita.objects.all().order_by('name')
    elif minute % 3 == 0:
        receitas = receita.objects.all().order_by('timestamp').reverse()
    elif minute % 7 == 0:
        receitas = receita.objects.all().order_by('name').reverse()
    elif minute % 11 == 0:
        receitas = receita.objects.all().order_by('ingredientes')
    else:
        receitas = receita.objects.all().order_by('likes').reverse()
    for tms in receitas:
        tms.timestamp = datetime.fromtimestamp(float(tms.timestamp))
    p = Paginator(receitas,6)
    page = request.GET.get('page')        
    receitass = p.get_page(page)
    return render(request,"decidir/index.html",{
        "receitas": receitass
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "decidir/login.html",{
                "message":"Inválido username e/ou senha."
            })
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    
    return render(request, "decidir/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        passwordconf = request.POST['passwordconf']

        if not username or not email or not password or not passwordconf:
            return render(request, "decidir/register.html", {
                "message": "Todos os campos precisam ser preenchidos."
            })
        if password != passwordconf:
            return render(request, "decidir/register.html", {
                "message": "Senhas precisam ser iguais."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "decidir/register.html", {
                "message": "Username já está em uso."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "decidir/register.html")
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def info(request, content, id):
    if content == "receita":
        recipe = receita.objects.get(pk=id)
        if not id:
            return JsonResponse(
                {
                "error": "Id da receita deve ser fornecido."
                }, status=400)
        recepuni = recipe.serialize()
        imgs = []
        for img in recepuni["img"].all():
            if "/media/images/" in img.img.url:
                imgs.append(img.img.url)
                print(img.img.url)
            else:
                print(img.img)
                url = str(img.img)
                imgs.append(url)
        recepuni["img"] = imgs
        return JsonResponse(recepuni,status=200)
    pass
@login_required
def create_recipe(request):
    if request.method == 'POST':
        #data = json.loads(request.body)
        #calorias = float(data.get("calorias", ""))
        #gorduras = float(data.get("gorduras", ""))
        #proteinas = float(data.get("proteinas", ""))
        #carboidratos = float(data.get("carboidratos", ""))
        nutricion = request.POST["nutricion"]
        foods = request.POST["foods"]
        imgs = request.FILES.getlist('images')
        name = request.POST["name"]
        modoPreparo = request.POST["modopreparo"]
        nutricion = nutricion.split(",")
        if not nutricion or not foods or not imgs or not name:
            return render(request, "decidir/recipe.html", {
                "message": "Todos os campos precisam ser preenchidos."
            })

        calorias = float(nutricion[0])
        carboidratos = float(nutricion[1])
        proteinas = float(nutricion[2])
        gorduras = float(nutricion[3])

        tranlator = Translator()
        translations = tranlator.translate(foods, dest='pt')
        translations = translations.text.split("\n")
        comidas = ''
        for i in range(0,(len(translations))):
            if i == (len(translations)-1):
                comidas += ' e '
            comidas += (translations[i])
            if i == (len(translations)-1):
                comidas += '.'
            elif i != (len(translations)-2):
                comidas += ', '
        recipe = receita.objects.create(name = name, ingredientes = comidas, calorias = calorias, carboidratos = carboidratos, proteinas = proteinas, gorduras = gorduras, timestamp = datetime.timestamp(datetime.now()), sender = request.user,modoPreparo = modoPreparo)
        recipe.save()
        for img in imgs:
            image = Img.objects.create(img = img)
            recipe.img.add(image)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.id:
            return render(request, "decidir/recipe.html")

@login_required
@csrf_exempt
def tradutor(request):
    if request.method == 'POST':
        tranlator = Translator()
        data = json.loads(request.body)
        translate = data.get("traduzir","")
        lang = data.get("lang","")
        translations = tranlator.translate(translate, dest=lang)

        return JsonResponse({"traducao":translations.text}, status=200)

    return HttpResponse(401)
@login_required
@csrf_exempt
def likes(request):
    if request.user.id is None:
        return HttpResponse(401)
    data = json.loads(request.body)
    user = request.user
    recipe_id = int(data.get("id",""))
    recipe = receita.objects.get(pk=recipe_id)
    if request.method == "POST":
        if user in recipe.likes.all():
            recipe.likes.remove(user)
            return JsonResponse({'receita_id': recipe_id}, status=202)
        else:
            recipe.likes.add(user)
            return JsonResponse({'receita_id': recipe_id}, status=202)
    return HttpResponse(401)

@login_required
def MinhasReceitas(request):
    receitas = receita.objects.filter(sender = request.user).order_by('timestamp').reverse()
    for tms in receitas:
        tms.timestamp = datetime.fromtimestamp(float(tms.timestamp))
    p = Paginator(receitas,6)
    page = request.GET.get('page')        
    receitass = p.get_page(page)
    return render(request,"decidir/Minhasreceitas.html",{
        "receitas": receitass
    })