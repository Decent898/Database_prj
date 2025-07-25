from django import template
import random

register = template.Library()

@register.filter
def split(value, arg):
    """
    将字符串按指定分隔符分割成列表
    用法：{{ value|split:',' }}
    """
    return value.split(arg)

@register.filter
def random_item(value):
    """
    从列表中随机选择一项
    用法：{{ list_value|random }}
    """
    if not value:
        return ''
    return random.choice(value)

@register.filter
def multiply(value, arg):
    """
    将数值乘以指定的参数
    用法：{{ value|multiply:100 }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0
