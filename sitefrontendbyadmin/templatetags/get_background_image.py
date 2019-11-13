from django import template
from sitefrontendbyadmin.models import BackgroundImage

register = template.Library()



@register.simple_tag()
def get_background_image():
    bg_image = BackgroundImage.objects.first()
    return bg_image