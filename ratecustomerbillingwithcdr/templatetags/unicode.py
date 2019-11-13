from django import template
import json

register = template.Library()

@register.simple_tag()
def decode_json(data):
	val = data.replace('[', '')
	val = val.replace(']', '')
	val = val.split(',')
	return val[0]
