from django.template.defaulttags import register
from django import template

register = template.Library()

@register.simple_tag(name = "define")
def define(val=None):
  return val


@register.filter(name='lookup')
def get_item(dictionary, key):
    return dictionary.get(key)
