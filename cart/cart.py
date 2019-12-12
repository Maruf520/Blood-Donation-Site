from decimal import Decimal
from django.conf import settings
from blood.models import Bank, Blood


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, blood, quantity=1, update_quantity=False):
        blood_id = str(blood.id)
        max_quantity = Blood.objects.get(id=blood.id).stock
        if blood_id not in self.cart:
            self.cart[blood_id] = {
                'quantity': 0, 'price': str(blood.price)}
        if update_quantity and self.cart[blood_id]['quantity'] <= max_quantity:
            self.cart[blood_id]['quantity'] = quantity
        elif int(self.cart[blood_id]['quantity']+quantity) <= max_quantity:
            self.cart[blood_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, blood):
        blood_id = str(blood.id)
        if blood_id in self.cart:
            del self.cart[blood_id]
            self.save()

    def __iter__(self):
        blood_ids = self.cart.keys()
        bloods = Blood.objects.filter(id__in=blood_ids)
        for blood in bloods:
            self.cart[str(blood.id)]['blood'] = blood

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
