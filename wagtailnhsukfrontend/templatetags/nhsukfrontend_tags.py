from django import template

register = template.Library()


@register.inclusion_tag('wagtailnhsukfrontend/breadcrumb.html', takes_context=True)
def breadcrumb(context):
    """
    Generates an array of pages which are passed to the breadcrumb template.
    """
    page = context['page']
    site = page.get_site()
    breadcrumb_pages = []

    # Traverse the page parents with get_parent() until we hit a site root
    while page.id != site.root_page_id and not page.is_root():
        page = page.get_parent()
        breadcrumb_pages = [page] + breadcrumb_pages

    return {
        'breadcrumb_pages': breadcrumb_pages,
    }


@register.inclusion_tag('wagtailnhsukfrontend/pagination.html', takes_context=True)
def pagination(context):
    """
    Calculates previous and next page values which are passed to the pagination template.
    """
    page = context['page']
    request = context['request']

    prev = page.get_prev_siblings().live().first()
    next = page.get_next_siblings().live().first()

    template_context = {}

    if prev:
        template_context['prev_label'] = prev.title
        template_context['prev_url'] = prev.get_url(request)
    if next:
        template_context['next_label'] = next.title
        template_context['next_url'] = next.get_url(request)

    return template_context


@register.inclusion_tag('wagtailnhsukfrontend/contents_list.html', takes_context=True)
def contents_list(context):
    """
    Generates a queryset of sibling pages which are passed to the contents_list template
    """
    page = context['page']
    request = context['request']

    sibling_pages = page.get_siblings().live()
    links = [
        {
            'label': sibling.title,
            'href': sibling.get_url(request),
            'is_current': sibling.id == page.id,
        }
        for sibling in sibling_pages
    ]

    return {
        'links': links,
    }


@register.filter
def chunk(input_list, size):
    """
    Split a list into a list-of-lists.
    If size = 2, [1, 2, 3, 4, 5, 6, 7] becomes [[1,2], [3,4], [5,6], [7]]
    """

    return [input_list[i:i + size] for i in range(0, len(input_list), size)]


@register.simple_tag
def promo_group_column_class(column_size):
    if column_size == 2:
        return 'nhsuk-grid-column-one-half'
    elif column_size == 3:
        return 'nhsuk-grid-column-one-third'
    else:
        raise Exception("promo column sizes must be either 2 or 3")
