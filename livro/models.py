from django.db import models
from datetime import date
import datetime
from usuarios.models import Usuario
from django.utils.text import slugify

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nome


class Livros(models.Model):
    nome = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 30)
    co_autor = models.CharField(max_length = 30, blank = True)
    data_cadastro = models.DateField(default = date.today)
    emprestado = models.BooleanField(default=False)
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


class Emprestimos(models.Model):
    choices = (
        ('P', 'Péssimo'),
        ('R', 'Ruim'),
        ('B', 'Bom'),
        ('O', 'Ótimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING, blank = True, null = True)
    nome_emprestado_anonimo = models.CharField(max_length = 30, blank = True)
    data_emprestimo = models.DateField(default = datetime.datetime.now)
    data_devolucao = models.DateField(blank = True, null = True)
    livro = models.ForeignKey(Livros, on_delete = models.DO_NOTHING)
    avaliacao = models.CharField(max_length = 1, choices = choices, blank = True, null = True)

    class Meta:
        verbose_name = 'Emprestimo'

    def __str__(self) -> str:
        return f'{self.nome_emprestado or self.nome_emprestado_anonimo} | {self.livro}'
