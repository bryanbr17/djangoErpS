from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica dos valores"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide dos valores"""
    try:
        if Decimal(str(arg)) == 0:
            return 0
        return Decimal(str(value)) / Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, arg):
    """Resta dos valores"""
    try:
        return Decimal(str(value)) - Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def add_decimal(value, arg):
    """Suma dos valores decimales"""
    try:
        return Decimal(str(value)) + Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, percent):
    """Calcula el porcentaje de un valor"""
    try:
        return Decimal(str(value)) * Decimal(str(percent)) / 100
    except (ValueError, TypeError):
        return 0
