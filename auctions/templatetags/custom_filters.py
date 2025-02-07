from django import template

register = template.Library()

def money_format(val):
    return f'${val:,.2f}'


register.filter('money_format', money_format)