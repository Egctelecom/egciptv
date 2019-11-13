from django import template
from rateareacode.models import Ratewithareacode
register = template.Library()

@register.simple_tag()
def check_number(num):
    number = num[:5]
    return number


@register.simple_tag()
def check_number2(num):
    number = num[:3]
    return number


@register.simple_tag()
def is_number_plus(num):
    number = num[:1]
    return number


@register.simple_tag()
def is_rate_code_chart_plus(num):
    number = num[-3:]
    if number is None:
        return 'No Value'
    else:
        try:
            rate_with_area = Ratewithareacode.objects.values('id', 'country_id', 'province_id', 'area_code', 'rate',
                                                             'status').filter(area_code=number)
            return rate_with_area[0]['rate']
        except:
            return 0


@register.simple_tag()
def is_rate_code_chart(num):
    if num is None:
        return 'No Value'
    else:
        try:
            rate_with_area = Ratewithareacode.objects.values('id', 'country_id', 'province_id', 'area_code', 'rate',
                                                             'status').filter(area_code=num)
            return rate_with_area[0]['rate']
        except:
            return 0


@register.simple_tag()
def plus_cost(rate, duration):
    total_rate = float(rate) * float(duration)
    return total_rate


@register.simple_tag()
def cost(rate, duration):
    total_rate = float(rate) * float(duration)
    return total_rate


@register.simple_tag()
def check_source_number_as_customer_number(source):
    number = num[:7]
    return number
