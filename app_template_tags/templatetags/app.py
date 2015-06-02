from django import template

register = template.Library()


@register.filter()
def message_tag_to_bootstrap_alert(value):
    if value == 'error':
        return 'danger'
    elif value == 'debug':
        return 'info'
    else:
        return value
