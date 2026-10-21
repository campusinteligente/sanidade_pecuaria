from django import template

register = template.Library()


@register.filter
def get_attr(obj, attr_name):
    """Permite acessar um campo do objeto cujo nome vem de uma variável.
    Uso no template: {{ objeto|get_attr:"nome_do_campo" }}
    """
    valor = getattr(obj, attr_name, "")
    if callable(valor):
        valor = valor()
    return valor
