from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def icon(name="", size="1em", class_name="", **kwargs):
    """Template tag para mostrar íconos de Bootstrap Icons"""
    icon_classes = f"bi bi-{name}"
    if class_name:
        icon_classes += f" {class_name}"

    style = f"font-size: {size};"
    attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items() if value is not None])

    return format_html(
        f'<i class="{icon_classes}" style="{style}" {attrs}></i>',
        icon_classes=icon_classes,
        style=style,
        attrs=attrs
    )

@register.simple_tag
def badge(text="", variant="primary", pill=False, class_name="", **kwargs):
    """Template tag para mostrar badges"""
    badge_classes = "badge"

    # Variants
    variant_map = {
        "primary": "bg-primary",
        "secondary": "bg-secondary",
        "success": "bg-success",
        "danger": "bg-danger",
        "warning": "bg-warning text-dark",
        "info": "bg-info text-dark",
        "light": "bg-light text-dark",
        "dark": "bg-dark"
    }

    badge_classes += f" {variant_map.get(variant, 'bg-primary')}"

    if pill:
        badge_classes += " rounded-pill"

    if class_name:
        badge_classes += f" {class_name}"

    attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items() if value is not None])
    return format_html(
        badge_classes=badge_classes,
        text=text,
        attrs=attrs
    )

@register.inclusion_tag('atomic/molecules/_form_group.html')
def form_group(type="text", id="", name="", label="", placeholder="", required=False, help_text="", **kwargs):
    """Template tag para mostrar grupos de formulario"""
    return {
        'form_group': {
            'type': type,
            'id': id,
            'name': name,
            'label': label,
            'placeholder': placeholder,
            'required': required,
            'help_text': help_text,
            'kwargs': kwargs,
            'content': kwargs.pop('content', '')
        }
    }

@register.inclusion_tag('atomic/molecules/_card.html')
def card(title="", subtitle="", class_name="", header_class="", body_class="", footer_class="", **kwargs):
    """Template tag para mostrar tarjetas"""
    return {
        'card': {
            'title': title,
            'subtitle': subtitle,
            'class': class_name,
            'header_class': header_class,
            'body_class': body_class,
            'footer_class': footer_class,
            'kwargs': kwargs,
            'content': kwargs.pop('content', '')
        }
    }

@register.inclusion_tag('atomic/molecules/_alert.html')
def alert(message="", variant="info", dismissible=False, class_name="", **kwargs):
    """Template tag para mostrar alertas"""
    return {
        'alert': {
            'message': message,
            'variant': variant,
            'dismissible': dismissible,
            'class': class_name,
            'kwargs': kwargs,
            'content': kwargs.pop('content', '')
        }
    }

@register.inclusion_tag('atomic/organisms/_header.html')
def header(brand_name="Setel", brand_url="dashboard:index", user=None, **kwargs):
    """Template tag para mostrar el header/navbar"""
    return {
        'brand_name': brand_name,
        'brand_url': brand_url,
        'user': user,
        'kwargs': kwargs
    }

@register.inclusion_tag('atomic/organisms/_footer.html')
def footer(company_name="Setel", year="", **kwargs):
    """Template tag para mostrar el footer"""
    return {
        'company_name': company_name,
        'year': year,
        'kwargs': kwargs
    }
