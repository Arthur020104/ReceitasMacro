from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    pass
class Img(models.Model):
    img = models.CharField(max_length=500)

class receita(models.Model):
    name = models.CharField(max_length=50)
    img = models.ManyToManyField(Img,blank=True,related_name="imgs")
    ingredientes = models.CharField(max_length=800)
    calorias = models.FloatField(validators=[MinValueValidator(100)])
    carboidratos = models.FloatField()
    proteinas = models.FloatField()
    gorduras = models.FloatField()
    timestamp = models.CharField(max_length=30)
    likes = models.ManyToManyField(User,blank=True,related_name="liked")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sender")
    modoPreparo = models.CharField(max_length=3000)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "ingredientes": self.ingredientes,
            "calorias": self.calorias,
            "carboidratos": self.carboidratos,
            "proteinas": self.proteinas,
            "gorduras": self.gorduras,
            "timestamp": self.timestamp,
            "likes": self.likes.all().count(),
            "sender": self.sender.username,
            "modoPreparo": self.modoPreparo
        }

