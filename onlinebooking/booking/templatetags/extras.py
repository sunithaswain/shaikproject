from django import template

register = template.Library()

@register.filter
def get_at_index(list1, index):
    return list1[index]