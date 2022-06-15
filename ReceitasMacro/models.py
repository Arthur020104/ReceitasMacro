from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    pass
class Img(models.Model):
    img = models.ImageField(null=False,blank=False, upload_to="images/")
    def __str__(self):
        return f"{self.id}: {self.img.url}"

class Label(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.id}: {self.name}"


class receita(models.Model):
    name = models.CharField(max_length=80)
    img = models.ManyToManyField(Img,blank=True,related_name="imgs")
    ingredientes = models.CharField(max_length=800)
    calorias = models.FloatField(validators=[MinValueValidator(100)])
    carboidratos = models.FloatField()
    proteinas = models.FloatField()
    gorduras = models.FloatField()
    timestamp = models.CharField(max_length=30)
    rawingredientes_pt = models.CharField(max_length=800,blank=False)
    likes = models.ManyToManyField(User,blank=True,related_name="liked")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    modoPreparo = models.CharField(max_length=3000)
    label = models.ManyToManyField(Label,blank=True,related_name="receita")

    def __str__(self):
        return f"{self.id}: {self.name}| Sender: {self.sender.username}"
    def serialize(self):
        timestamp = datetime.fromtimestamp(float(self.timestamp)).strftime("%d %B, %Y")
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "ingredientes": self.ingredientes,
            "calorias": self.calorias,
            "carboidratos": self.carboidratos,
            "proteinas": self.proteinas,
            "gorduras": self.gorduras,
            "timestamp": timestamp,
            "likes": self.likes.all().count(),
            "sender": self.sender.username,
            "modoPreparo": self.modoPreparo
        }
class Meta:
        app_label = 'ReceitaMacro' 

