from django.shortcuts import render


from django.http import HttpResponseRedirect
from main.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Create your views here.

# def main(request):
#     cart = SneakersCart.objects.all()
#     brand = Brand.objects.all()
#     searched_sneakers = request.POST.get('search')
#     product = SneakersCart.objects.filter(title__contains = searched_sneakers)
#     return render(request, 'index.html', {'cart': cart, 'brand': brand, 'product': product})

def main(request):
    card = SneakersCart.objects.all()
    brand = Brand.objects.all()
    return render(request, 'index.html', {'brand':brand, 'card':card})

def search(request):
    if request.method == 'POST':
        searched_sneakers = request.POST.get('search').title()
        product = SneakersCart.objects.filter(title__contains = searched_sneakers)
        return render(request, 'search.html', {'product': product})

def more(request, id):
    try:
        more = SneakersCart.objects.get(id=id)
        return render(request, 'more.html', {'more': more})
    except:
        return render(request, 'error.html')

res = {}
def addCart(request, pk):
    try:
        cart_session = request.session.get('cart_session', [])
        cart_session.append(pk)
        request.session['cart_session'] = cart_session
        return HttpResponseRedirect('/')
    except:
        return render(request, 'error.html')

def cart(request):
    cart_session = request.session.get('cart_session', [])
    count_of_product = len(cart_session)
    products_cart = SneakersCart.objects.filter(id__in=cart_session)
    all_products_sum = 0
    for i in products_cart:
        i.count = cart_session.count(i.id)
        i.sum = i.count * i.price
        all_products_sum += i.sum
    return render(request, 'cart.html', {'products_cart': products_cart, 'count_of_product': count_of_product, 'all_products_sum' :all_products_sum})

# def removeCart(request, id):
#     cart_session = request.session.get('cart_session', [])
#     carts = []
#     for pk in cart_session:
#         if pk != id:
#             carts.append(pk)
#     request.session['cart_session'] = carts
#     return HttpResponseRedirect('/cart')

# def removeCart(request, id):
#     cart_session = request.session.get('cart_session', [])
#     carts = cart_session
#     num = carts.index(id)
#     carts.pop(num)
#     request.session['cart_session'] = carts
#     return HttpResponseRedirect('/cart')

def removeCart(request, id):
    cart_session = request.session.get('cart_session', [])
    carts = cart_session
    carts.remove(id)
    request.session['cart_session'] = carts
    return HttpResponseRedirect('/cart')

def about_us(request):
    return render(request, 'about.html')

def signUp(request):
    try:
        if request.method == 'POST':
            user = UserCreationForm(request.POST)
            if user.is_valid():
                user.save()
                return HttpResponseRedirect('/')
        else:
            user = UserCreationForm()
        return render(request, 'register.html', {'user': user})
    except:
        return render(request, 'error.html')

def signIn(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request , username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            form = AuthenticationForm()
        return render(request, 'register.html', {'user': form})
    except:
        return render(request, 'error.html')

def signOut(request):
    logout(request)
    return HttpResponseRedirect('/')


def order(request):
    cart_session = request.session.get('cart_session', [])
    if request.method == 'POST':
        if len(cart_session) == 0:
            messages.error(request, 'Ваша корзина пуста', extra_tags='danger')
            return HttpResponseRedirect('/cart')
        else:
            customer = Customer()
            customer.name = request.POST.get('c_name')
            customer.last_name = request.POST.get('c_lastname')
            customer.number = request.POST.get('c_number')
            customer.address = request.POST.get('c_addres')
            customer.message = request.POST.get('c_message')
            customer.save()
            for i in range(len(cart_session)):
                order= Order()
                cart_session = request.session.get('cart_session', [])
                cart_session_lst = cart_session
                set_list = set(cart_session_lst)
                product_names_add_counts = []
                for i in set_list:
                    product = SneakersCart.objects.get(id = i)
                    product_name = product.title
                    count = cart_session_lst.count(i)
                    products = f'{product_name} - {count}'
                    product_names_add_counts.append(products)
                products_cart = SneakersCart.objects.filter(id__in = cart_session)
                all_products_sum = 0
                for i in products_cart:
                    i.count = cart_session.count(i.id)
                    i.sum = i.count * i.price
                    all_products_sum += i.sum
                order.product = product_names_add_counts
                order.customer = customer
                order.total_price = all_products_sum
                order.phone = customer.number
                order.address = customer.address
                order.save()

            request.session['cart_session'] = []
            messages.error(request, 'Заказ успешно отправлён!', extra_tags='success')
            return HttpResponseRedirect('/cart')