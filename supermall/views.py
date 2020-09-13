import json
from math import ceil

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from .models import Product, Contact, Order, OrderUpdate


def index(request):
    all_products = []
    categorized_Products = Product.objects.values('category', 'id')
    categories = {item['category'] for item in categorized_Products}
    for category in categories:
        products = Product.objects.filter(category=category)
        numofproduct = len(products)
        nSlides = numofproduct // 4 + ceil((numofproduct / 4) - (numofproduct // 4))
        all_products.append([products, range(1, nSlides), nSlides])
    # products = Product.objects.all()
    #
    # # params = {'no_of_slides': nSlides, 'range': range(1,nSlides), 'products': products}
    # allProds = [[products, range(1,nSlides), nSlides],\
    #             [products, range(1,nSlides), nSlides]]
    params = {'allProducts': all_products}
    return render(request, 'supermall/supermall_index.html', params)


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search').lower()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": "", 'query': query}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'supermall/search.html', params)


def about(request):
    return render(request, 'supermall/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'supermall/contact.html', {'thank': thank})


def track(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_description, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'supermall/track.html')


def product_view(request, prod_id):
    product = Product.objects.filter(id=prod_id)
    return render(request, 'supermall/product_view.html',
                  {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        postal_code = request.POST.get('postal_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                      postal_code=postal_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_description="The order has been placed")
        update.save()
        thank = True
        order_id = order.order_id
        return render(request, 'supermall/checkout.html', {'thank': thank, 'id': order_id})
    return render(request, 'supermall/checkout.html')
