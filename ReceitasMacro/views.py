
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User, receita, Img, Label
import json
from googletrans import Translator
from datetime import datetime
from PIL import Image
from pathlib import Path
import os

def index(request):
    minute = int(datetime.now().strftime("%M"))
    receitas = receita.objects.filter(public=True).order_by('likes').reverse()
    for tms in receitas:
        tms.timestamp = datetime.fromtimestamp(float(tms.timestamp))
    p = Paginator(receitas,6)
    page = request.GET.get('page')
    receitass = p.get_page(page)
    print(Path(os.getcwd()))
    return render(request,"ReceitasMacro/index.html",{
        "receitas": receitass
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "ReceitasMacro/login.html",{
                "message":"Inválido username e/ou senha."
            })
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    return render(request, "ReceitasMacro/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        passwordconf = request.POST['passwordconf']

        if not username or not email or not password or not passwordconf:
            return render(request, "ReceitasMacro/register.html", {
                "message": "Todos os campos precisam ser preenchidos."
            })
        if password != passwordconf:
            return render(request, "ReceitasMacro/register.html", {
                "message": "Senhas precisam ser iguais."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ReceitasMacro/register.html", {
                "message": "Username já está em uso."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "ReceitasMacro/register.html")
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def info(request, content, id):
    if content == "receita":
        Receita = receita.objects.get(pk=id)
        if not request.user == Receita.sender:
            recipe = receita.objects.get(pk=id,public=True)
        else:
            recipe = Receita
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
            else:
                url = str(img.img)
                imgs.append(url)
        recepuni["img"] = imgs
        return JsonResponse(recepuni,status=200)
    pass
@login_required
def create_recipe(request):
    if request.method == 'POST':
        labels = []
        for item in Label.objects.all():
            labels.append(item.name)
        my_lables = []
        for post in request.POST:
            if post in labels:
                my_lables.append(Label.objects.get(name=post))
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
        rendimento = request.POST["rendimento"]
        nutricion = nutricion.split(",")
        if not nutricion or not foods or not imgs or not name or not rendimento:
            return render(request, "ReceitasMacro/recipe.html", {
                "message": "Todos os campos precisam ser preenchidos.",
                "labels": Label.objects.all()
            })
        calorias = float(nutricion[0])
        carboidratos = float(nutricion[1])
        proteinas = float(nutricion[2])
        gorduras = float(nutricion[3])

        tranlator = Translator()
        translations = tranlator.translate(foods, dest='pt')
        rawingredientes = translations.text
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
        recipe = recipe = receita.objects.create(name = name, ingredientes = comidas, calorias = calorias, carboidratos = carboidratos, proteinas = proteinas, gorduras = gorduras, timestamp = datetime.timestamp(datetime.now()), sender = request.user,modoPreparo = modoPreparo,rawingredientes_pt = rawingredientes, rendimento = rendimento)
        recipe.save()
        for img in imgs:
            image = Img.objects.create(img = img)
            convert_to_webp(Path(os.getcwd()+f"/ReceitasMacro/media/images/{img.name}"))
            recipe.img.add(image)
        for label in my_lables:
            recipe.label.add(label)
        return HttpResponseRedirect(reverse("MinhasReceitas"))
    else:
        if request.user.id:
            label = Label.objects.all()
            return render(request, "ReceitasMacro/recipe.html",{
                "labels":label
            })

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
def MinhasReceitas(request,*args):
    message = None
    if args:
        message = {'msg':args[0],'role':args[1]}
    receitas = receita.objects.filter(sender = request.user).order_by('timestamp').reverse()
    for tms in receitas:
        tms.timestamp = datetime.fromtimestamp(float(tms.timestamp))
    p = Paginator(receitas,4)
    page = request.GET.get('page')
    receitass = p.get_page(page)
    return render(request,"ReceitasMacro/Minhasreceitas.html",{
        "receitas": receitass,'mesage':message
    })

@csrf_exempt
def buscar(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content","")
        filtro = data.get("filtro","")
        if filtro != "Filtros":
            filtro = Label.objects.get(pk=filtro).id
        receitas = receita.objects.filter(name__icontains=content, public=True)
        receitar = []
        for recepi in receitas:
            filtros = []
            if filtro != "Filtros":
                for item in recepi.label.all():
                    filtros.append(item.id)
                if filtro in filtros:
                    recepi = recepi.serialize()
                    imgs = []
                    for img in recepi["img"].all():
                        if "/media/images/" in img.img.url:
                            imgs.append(img.img.url)
                        else:
                            url = str(img.img)
                            imgs.append(url)
                    recepi["img"] = imgs
                    receitar.append(recepi)
            else:
                recepi = recepi.serialize()
                imgs = []
                for img in recepi["img"].all():
                    if "/media/images/" in img.img.url:
                        imgs.append(img.img.url)
                    else:
                        url = str(img.img)
                        imgs.append(url)
                recepi["img"] = imgs
                receitar.append(recepi)
        return JsonResponse(receitar, status=202, safe=False)

    return render(request, "ReceitasMacro/busca.html",{
                "labels":Label.objects.all()
            })


def convert_to_webp(source):
    """Convertendo imagem para Webp.
    para eonomizar espaco de memoria
    """
    image = Image.open(source)  # Open image
    image.save(source, format="webp")  # Convert image to webp

#@login_required
def delreceita(request,id):
    Receita = get_object_or_404(receita,pk=id)
    if Receita.sender == request.user:
        imgs1 = Receita.img.all()
        for img in imgs1:
            if img.img.url:
                #print(Path(os.getcwd()+img.img.url))
                try:
                    os.remove(Path(os.getcwd()+'/ReceitasMacro'+img.img.url))
                except:
                    print("An exception occurred")
            img.delete()
        Receita.delete()
        print(reverse('MinhasReceitas'))
        return MinhasReceitas(request,'Receita deletada com sucesso','warning')
    else:
        return HttpResponseRedirect(reverse('index'))
def editreceita(request,id):
    if request.method == 'POST':
        Receita = receita.objects.get(pk=id)
        labels = []
        for item in Label.objects.all():
            labels.append(item.name)
        my_lables = []
        for post in request.POST:
            if post in labels:
                my_lables.append(Label.objects.get(name=post))
        nutricion = request.POST["nutricion"]
        foods = request.POST["foods"]
        imgs = request.FILES.getlist('images')
        name = request.POST["name"]
        modoPreparo = request.POST["modopreparo"]
        rendimento = request.POST["rendimento"]
        nutricion = nutricion.split(",")
        if not nutricion or not foods or not name:
            return render(request, "ReceitasMacro/editReceita.html", {
                "message": "Todos os campos precisam ser preenchidos.",
                'receita':Receita,
                "labels": Label.objects.all()
            })

        tranlator = Translator()
        translations = tranlator.translate(foods, dest='pt')
        rawingredientes_pt = translations.text
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
        Receita.name = name
        if not rawingredientes_pt == Receita.rawingredientes_pt:
            Receita.rawingredientes_pt = rawingredientes_pt
            calorias = float(nutricion[0])
            carboidratos = float(nutricion[1])
            proteinas = float(nutricion[2])
            gorduras = float(nutricion[3])
            Receita.ingredientes = comidas
            Receita.calorias = calorias
            Receita.carboidratos = carboidratos
            Receita.proteinas = proteinas
            Receita.gorduras = gorduras
        Receita.rendimento = rendimento
        Receita.timestamp = datetime.timestamp(datetime.now())
        Receita.modoPreparo = modoPreparo
        if imgs:
            imgs1 = Receita.img.all()
            for img in imgs1:
                if img.img.url:
                    #print(Path(os.getcwd()+img.img.url))
                    try:
                        os.remove(Path(os.getcwd()+'/ReceitasMacro'+img.img.url))
                    except:
                        print("An exception occurred")
                img.delete()
            for img in imgs:
                image = Img.objects.create(img = img)
                convert_to_webp(Path(os.getcwd()+f"/ReceitasMacro/media/images/{img.name}"))
                Receita.img.add(image)

        for categoria in Receita.label.all(): Receita.label.remove(categoria)
        for label in my_lables:
            Receita.label.add(label)
        Receita.save()
        return HttpResponseRedirect(reverse("MinhasReceitas"))

    Receita = get_object_or_404(receita,pk=id)
    if Receita.sender == request.user:
        return render(request,'ReceitasMacro/editReceita.html',{'receita':Receita,"labels": Label.objects.all()})