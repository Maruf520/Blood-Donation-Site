from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.views.decorators.cache import never_cache
from blood.models import Bank, Blood
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect

decorators = [never_cache, login_required]


@never_cache
def order_create(request):
    cart = Cart(request)
    a = cart.get_total_price()
    print("total cost", cart.get_total_price())
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, initial={
                               'total_cost': cart.get_total_price()})
        print(cart.get_total_price())
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['blood'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                previous_blood = Blood.objects.get(
                    id=item['blood'].id)
                print("blood stock", previous_blood.stock)
                previous_blood.stock = previous_blood.stock - item['quantity']
                previous_blood.save()
            cart.clear()
            form = OrderCreateForm()

        return HttpResponseRedirect(reverse('orders:thank-giving', kwargs={'order_id': order.id}))
    else:
        form = OrderCreateForm(initial={'total_cost': cart.get_total_price()})
    return render(request, 'order/create.html', {'form': form})


def thank_giving(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'order/created.html', {'order': order})
