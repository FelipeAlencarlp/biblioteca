from datetime import datetime
from django import template

register = template.Library()

@register.filter # indica para o Django que essa função é um filtro
def mostra_duracao(value1, value2):
    # verificar se a instância é verdadeira
    if all((isinstance(value1, datetime), isinstance(value2, datetime))):
        dias = (value1 - value2).days
        texto = 'dias'
        if dias == 1:
            texto = 'dia'
        return (f"{dias} {texto}")
    
    return "Ainda não foi devolvido."