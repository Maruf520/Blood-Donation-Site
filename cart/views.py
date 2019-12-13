from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from blood.models import Blood
from django.forms import forms
from .cart import Cart
from .forms import CartAddBloodForm, CCartAddBloodForm
from django.views.decorators.cache import never_cache


# @require_POST
def cart_add(request, blood_id):
    # create a new cart object passing it the request object
    cart = Cart(request)
    blood = get_object_or_404(Blood, id=blood_id)
    # max_quantity = blood.stock
    form = CartAddBloodForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # if cd['quantity'] > max_quantity:
        #     return HttpResponse("hello! select less")
        cart.add(
            blood=blood, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, blood_id):
    cart = Cart(request)
    blood = get_object_or_404(Blood, id=blood_id)
    cart.remove(blood)
    return redirect('cart:cart_detail')


@never_cache
def cart_detail(request):
    cart = Cart(request)
    print("fuck", cart)
    # return HttpResponse("error")
    for item in cart:
        maximum_quantity = Blood.objects.get(id=item['blood'].id).stock
        # print("max", maximum_quantity, "  /",
        #       Blood.objects.get(id=item['blood'].id))
        BLOOD_QUANTITY_CHOICES = [(i, str(i))
                                  for i in range(1, maximum_quantity)]
        form = CCartAddBloodForm(
            BLOOD_QUANTITY_CHOICES, initial={'quantity': item['quantity'], 'update': True})
        # print("funk",   item['update_quantity_form'].is_valid())
        # if not form.is_valid():
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > 5:
                return HttpResponse("HEllo")
        item['update_quantity_form'] = form

    return render(request, 'cart/detail.html', {'cart': cart})
