from django import template

register = template.Library()


@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name, '')

# Replace underscores with spaces
@register.filter
def replace_underscores(value, replacement=' '):
    """Replaces underscores with space (or custom replacement)."""
    if isinstance(value, str):
        return value.replace('_', replacement)
    return value
