from django.shortcuts import render
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
#New version is buged so this one is fine
def index(request):
    minute = int(datetime.now().strftime("%M"))
    #fazendo ser diferente a ordenacao das receitas dependendo do minuto
    #ex: minuto 22 % 11 == 0->True entao a ordenacao sera pelos ingredientes
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
    #percorrendo por cada receita e tanformando o timestamp mais userfriendly
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
        #usuário inválido
        if user is None:
            return render(request, "decidir/login.html",{
                "message":"Inválido username e/ou senha."
            })
        #usuário válido
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
        #Identificando se cada dado é diferente de none(null)
        if not username or not email or not password or not passwordconf:
            return render(request, "decidir/register.html", {
                "message": "Todos os campos precisam ser preenchidos."
            })
        if password != passwordconf:
            return render(request, "decidir/register.html", {
                "message": "Senhas precisam ser iguais."
            })
        #tetando criar o usuário
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        #Se o username já estiver em uso o usuário nao será criado e retornará para o cliente a mensagem abaixo 
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
    #verificando se o conteúdo é o desejado
    if content == "receita":
        #verificando se foi fornecido o id da receita
        if not id:
            return JsonResponse(
                {
                "error": "Id da receita deve ser fornecido."
                }, status=400)
        #pegando a receita desejada
        recipe = receita.objects.get(pk=id)
        recepuni = recipe.serialize()
        imgs = []
        #serializing as imagens
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
        nutricion = request.POST["nutricion"]
        foods = request.POST["foods"]
        imgs = request.FILES.getlist('images')
        name = request.POST["name"]
        modoPreparo = request.POST["modopreparo"]
        nutricion = nutricion.split(",")
        #verifidando se os dados essenciais estao preenchidos
        #se nao retornando mensagem
        if not nutricion or not foods or not imgs or not name:
            return render(request, "decidir/recipe.html", {
                "message": "Todos os campos precisam ser preenchidos.",
                "labels": Label.objects.all()
            })
        labels = []
        #pegando o nome de cada label e guardando dentro da lista labels
        for item in Label.objects.all():
            labels.append(item.name)
        my_lables = []
        #percorrendo por todos os itens dentro do request.POST
        #e pegando os labels e colocando na lista my_lables
        for post in request.POST:
            if post in labels:
                my_lables.append(Label.objects.get(name=post))

        calorias = float(nutricion[0])
        carboidratos = float(nutricion[1])
        proteinas = float(nutricion[2])
        gorduras = float(nutricion[3])

        #traduzindo as comidas que estavam em ingles
        tranlator = Translator()
        translations = tranlator.translate(foods, dest='pt')
        translations = translations.text.split("\n")
        comidas = ''

        #percorrendo pela lista de strings de ingredientes
        #e adicionado pontucao
        for i in range(0,(len(translations))):
            if i == (len(translations)-1):
                comidas += ' e '
            comidas += (translations[i])
            if i == (len(translations)-1):
                comidas += '.'
            elif i != (len(translations)-2):
                comidas += ', '
        #criando a receita
        recipe = receita.objects.create(name = name, ingredientes = comidas, calorias = calorias, carboidratos = carboidratos, proteinas = proteinas, gorduras = gorduras, timestamp = datetime.timestamp(datetime.now()), sender = request.user,modoPreparo = modoPreparo)
        recipe.save()

        #criando as imgs e estabelecendo relacao com a receita
        for img in imgs:
            image = Img.objects.create(img = img)
            recipe.img.add(image)
        for label in my_lables:
            recipe.label.add(label)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.id:
            label = Label.objects.all()
            return render(request, "decidir/recipe.html",{
                "labels":label
            })

@login_required
@csrf_exempt
def tradutor(request):
    if request.method == 'POST':
        #traduzindo os ingredientes para ser possível a utilizacao da api de nutricao
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
    #checando novamente se o usuário nao é anônimo
    if request.user.id is None:
        return HttpResponse(401)

    if request.method == "POST":
        data = json.loads(request.body)
        #pegando o usuário e a receita
        user = request.user
        recipe_id = int(data.get("id",""))
        recipe = receita.objects.get(pk=recipe_id)
        #verificando se o usuário já deu like na receita 
        if user in recipe.likes.all():
            #removendo o usuário da lista de clientes que deram like
            recipe.likes.remove(user)
            return JsonResponse({'receita_id': recipe_id}, status=202)
        else:
            #adicionando o usuário da lista de clientes que deram like
            recipe.likes.add(user)
            return JsonResponse({'receita_id': recipe_id}, status=202)
    return HttpResponse(401)

@login_required
def MinhasReceitas(request):
    #selecionando as receitas que tem a relacao de sender com o usuário
    receitas = receita.objects.filter(sender = request.user).order_by('timestamp').reverse()
    #percorrendo por cada receita e tanformando o timestamp mais userfriendly
    for tms in receitas:
        tms.timestamp = datetime.fromtimestamp(float(tms.timestamp))
    p = Paginator(receitas,6)
    page = request.GET.get('page')        
    receitass = p.get_page(page)
    return render(request,"decidir/Minhasreceitas.html",{
        "receitas": receitass
    })

@csrf_exempt
def buscar(request):
    if request.method == "POST":
        #pegando o conteúdo da busca e o filtro
        data = json.loads(request.body)
        content = data.get("content","")
        filtro = data.get("filtro","")
        #Se existir filtro pegar o id do filtro pelo id fornecido
        if filtro:
            filtro = Label.objects.get(pk=filtro).id
        #pegando as receitas que o conteúdo da busca está no nome
        receitas = receita.objects.filter(name__contains=content)
        receitar = []
        #percorrendo por todas as receitas
        for recepi in receitas:
            filtros = []
            #verficando se existe o filtro
            if filtro:
                #pegando o filtro/label da receita
                for item in recepi.label.all():
                    filtros.append(item.id)
                #verificando se o filtro/label de busca é igual a algum da receita
                if filtro in filtros:
                    recepi = recepi.serialize()
                    imgs = []
                    #serializing as imagens
                    for img in recepi["img"].all():
                        if "/media/images/" in img.img.url:
                            imgs.append(img.img.url)
                        else:
                            url = str(img.img)
                            imgs.append(url)
                    recepi["img"] = imgs
                    #adicionando a receita a lista receitar
                    receitar.append(recepi)
            else:
                recepi = recepi.serialize()
                imgs = []
                #serializing as imagens
                for img in recepi["img"].all():
                    if "/media/images/" in img.img.url:
                        imgs.append(img.img.url)
                    else:
                        url = str(img.img)
                        imgs.append(url)
                recepi["img"] = imgs
                #adicionando a receita a lista receitar
                receitar.append(recepi)
        return JsonResponse(receitar, status=202, safe=False)

    return render(request, "decidir/busca.html",{
                "labels":Label.objects.all()
            })