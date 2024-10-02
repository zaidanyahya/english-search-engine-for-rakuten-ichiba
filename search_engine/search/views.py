from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from .utils import get_items_from_rakuten_api, get_item_from_rakuten_api


def search(request):
    return render(request, 'search/search.html')


def search_results(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))

    # get datas from api
    items = get_items_from_rakuten_api(query, page)

    # reach the last page ?
    has_next_page = len(items) > 0

    # no more items so redirect to first page
    if not has_next_page and page > 1:
        return redirect(reverse('search_results') + f'?q={query}&page=1&message=no_more_items')

    context = {
        'items': items,
        'query': query,
        'current_page': page,
        'has_next_page': has_next_page,
        'has_previous_page': page > 1,
        'no_more_items': request.GET.get('message') == 'no_more_items'
    }
    return render(request, 'search/results.html', context)


def item_detail(request, item_code):
    # get single item from rakuten api
    item = get_item_from_rakuten_api(item_code)
    context = {'item': item}
    return render(request, 'search/detail.html', context)
