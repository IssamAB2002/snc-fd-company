from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def update_query_params(context, **kwargs):
    # get the current request
    request = context['request']
    # update or add the new query parameters
    query_params = request.GET.copy()
    # check for each key & value in queries given as params
    for key, value in kwargs.items():
        # if value is not none set it to the given value or keep the old one
        if value is not None:
            # if the value is given the key = new value, else key = old value already in queries
            query_params[key] = value
        else:
            # if the value is none remove the key and value from queirs
            query_params.pop(key, None)
    # return the updated queries
    return '?' + urlencode(query_params)
