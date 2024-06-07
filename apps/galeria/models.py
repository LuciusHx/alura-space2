from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


#Cada classe é uma tabela no banco de dados
class Fotografia(models.Model):
    
    OPCOES_CATEGORIA = [
        ("NEBULOSA", "Nebulosa"),
        ("ESTRELA", "Estrela"),
        ("GALAXIA", "Galáxia"),
        ("PLANETA", "Planeta"),
    ]
    
    nome = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=150, null=False, blank=False)
    categoria = models.CharField(max_length=100, choices=OPCOES_CATEGORIA, default='')
    descricao = models.TextField(null=False, blank=False)
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    publicada = models.BooleanField(default=True)
    data_fotografia = models.DateTimeField(default=datetime.now, blank=False)
    usuario = models.ForeignKey( #Foreign Key é pra relacionar duas tabelas: 1,1 ; 1,n ; n,1 (banco de dados) 
        to=User, #Relacionar o "De um pra muitos"
        on_delete=models.SET_NULL,
        null=True,
        blank=False, #é obrigatório no formulário
        related_name='user', #nome para acessar objetos
    )
    
    def __str__(self):
        return self.nome
