from django import template

register = template.Library()

@register.filter # indica para o Django que essa função é um filtro
def mostra_duracao(value1, value2):
    return (value1 - value2).days