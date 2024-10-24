# import django template
from django import template
# define register as template library (must do)
register = template.Library()
# include register & set it as a simple tag


@register.simple_tag
# define custom pagination tag & set page object as params
def custom_pagination(page_obj):
    # define total page as pagination pages number
    total_pages = page_obj.paginator.num_pages
    # get last page as (total page)
    last_page = total_pages
    # get current page from page object
    current_page = page_obj.number
    # define page range for pagination nav & set it to empty
    page_range = []
    # check if cuurent page < or = 1
    if current_page <= 1:
        # check if total pages equals or less than 1
        if total_pages <= 1:
            # if yes let the range page be just the first page
            page_range = [1]
        else:
            # if yes page range = to [1] [2] [3] (probably)
            page_range = [1, current_page + 1, current_page + 2]
        # else if current page > 1 & < last page
    elif (current_page > 1 and current_page < total_pages):
        # if yes page range (example current page = 3) = [2] [3] [4]
        page_range = [current_page - 1, current_page,
                      current_page + 1]    # Context dictionary
    elif (current_page >= last_page):
        page_range = [last_page -1 -1, last_page - 1, last_page]
    show_first_page = True if current_page > 2 else False
    show_last_page = True if current_page < last_page - 2 else False
    print(show_last_page)
    context = {
        # last page
        'last_page': last_page,
        # list of page numbers to display
        'page_range': page_range,
        # the current page number
        'current_page': current_page,
        # check if there is a previous page
        'has_previous': page_obj.has_previous(),
        # previous page number
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        # check if there is a next page
        'has_next': page_obj.has_next(),
        # next page number
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'show_last_page': show_last_page,
        'show_first_page': show_first_page
    }

    return context
