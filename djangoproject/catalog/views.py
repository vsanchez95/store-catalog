from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from store_catalog.container import Container
from store_catalog.service_layer.services import ProductSearcher


@inject
def catalog_list(
        request: HttpRequest,
        product_searcher: ProductSearcher = Provide[Container.product_searcher],
) -> HttpResponse:
    """List Products.

    Args:
        request (HttpRequest): Django Http request.
        product_searcher: service to search products.

    Returns:
        HttpResponse: Django Http response.

    """
    # TODO: improve with more advanced searchs (only query_by product title for now)
    return render(
        request,
        template_name='catalog/catalog_list.html',
        context={
            'products': product_searcher(
                q=request.GET.get('query', '*'),
                query_by='title',
            ),
            'query': request.GET.get('query', ''),
        },
    )
