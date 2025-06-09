from django import template

register = template.Library()

@register.filter
def vndcomma(value):
    """
    Định dạng số thành tiền Việt Nam: 8.632.213
    """
    try:
        value = int(float(value))
        return '{:,}'.format(value).replace(',', '.')
    except:
        return value 