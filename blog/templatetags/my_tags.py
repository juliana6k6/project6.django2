from django import template


register = template.Library()


@register.filter()
def media_filter1(data):
    if data:
        return f"/media/{data}"
    return '#'
