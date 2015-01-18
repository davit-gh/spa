from mezzanine.pages.page_processors import processor_for
from .models import HomePage, Slide
from .models import Portfolio, PortfolioItem, PortfolioItemCategory
from django.http import HttpResponseRedirect
from django.conf import settings

@processor_for(Portfolio)
def portfolio_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    # get the Portfolio's items, prefetching categories for performance
    items = PortfolioItem.objects.published(
        for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=page)
    # filter out only cateogries that are user in the Portfolio's items
    categories = PortfolioItemCategory.objects.filter(
        portfolioitems__in=items).distinct()
    return {'items': items, 'categories': categories}


@processor_for(PortfolioItem)
def portfolioitem_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    portfolioitem = PortfolioItem.objects.published(
        for_user=request.user).prefetch_related(
        'categories', 'images').get(id=page.portfolioitem.id)
    return {'portfolioitem': portfolioitem}
import pdb
@processor_for(HomePage)
def home_processor(request, page):
    items = PortfolioItem.objects.published(
        for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=page.homepage.featured_portfolio)
    #pdb.set_trace()
    
    return {'items': items}

@processor_for('services')
def home_processor(request, page):
    #pdb.set_trace()
    items = PortfolioItem.objects.published().prefetch_related('categories')
    portitems = items.filter(parent=page)
    return {'portitems': portitems}

