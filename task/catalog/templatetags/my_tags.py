from django import template


register = template.Library()


@register.simple_tag
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"
