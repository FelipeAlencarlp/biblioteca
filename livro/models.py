from django.db import models
from datetime import date
from usuarios.models import Usuario
from django.utils.text import slugify

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()

    def __str__(self) -> str:
        return self.nome


class Livros(models.Model):
    nome = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 30)
    co_autor = models.CharField(max_length = 30, blank = True)
    data_cadastro = models.DateField(default = date.today)
    esprestado = models.BooleanField(default = False)
    nome_emprestado = models.CharField(max_length = 30, blank = True)
    data_emprestimo = models.DateTimeField(blank = True, null = True)
    data_devolucao = models.DateTimeField(blank = True, null = True)
    tempo_duracao = models.DateField(blank = True, null = True)
    categoria = models.ForeignKey(Categoria, on_delete = models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Livro'

    def __str__(self) -> str:
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)

            super().save(*args, **kwargs)
