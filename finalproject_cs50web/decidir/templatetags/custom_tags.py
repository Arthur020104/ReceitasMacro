from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
  return (int(val)%3)