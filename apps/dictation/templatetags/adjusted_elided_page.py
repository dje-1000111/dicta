from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def adjusted_elided_page(p, number, on_each_side=3, on_ends=2):
    """Show an elided number of pages separate by ... from each sides of numeration."""
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(
        number=number, on_each_side=on_each_side, on_ends=on_ends
    )
