from django.shortcuts import render
from .models import Product, Limit
from .forms import BasicSearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tasks import check_product, main
from django.http import HttpResponseRedirect


def home(request):
    #query
    all = request.GET.get('all')
    if all == 'All':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(added_by_scrap=False)
    limit = Limit.objects.last()

    #form
    form = BasicSearchForm(request.GET)

    #data
    index = request.GET.get('index')
    name = request.GET.get('name')
    ean = request.GET.get('ean')
    category = request.GET.get('category')
    price_st = request.GET.get('price_st')
    price_end = request.GET.get('price_end')
    count_st = request.GET.get('count_st')
    count_end = request.GET.get('count_end')

    if index:
        products = products.filter(index__icontains=index)
    if name:
        products = products.filter(name__icontains=name)
    if ean:
        products = products.filter(ean__icontains=ean)
    if category:
        products = products.filter(category__icontains=category)
    if price_st:
        products = products.filter(price__gte=price_st)
    if price_end:
        products = products.filter(price__lte=price_end)
    if count_st:
        products = products.filter(count__gte=count_st)
    if count_end:
        products = products.filter(count__lte=count_end)

    #paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    context = {'products': products,
               'numbers': numbers,
               'limit': limit,
               'form': form}
    return render(request, 'home.html', context)


def send(request):
    products = Product.objects.all()
    check_product()
    return HttpResponseRedirect('/')


def delete(request):
    products = Product.objects.all()
    for item in products:
        item.delete()
    return HttpResponseRedirect('/')


def scrap(request):
    main(type=True)
    return HttpResponseRedirect('/')


