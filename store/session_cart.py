from goods.models import Goods


class SessionCartManager:
    kname = 'cart'

    @staticmethod
    def _make_unit(goods_pk, quantity=1):
        return {'goods_pk': int(goods_pk), 'quantity': int(quantity)}

    @staticmethod
    def add_unit(cart_list, goods_pk, quantity=1):
        goods_pk = int(goods_pk)
        quantity = int(quantity)

        for cart_unit in cart_list:
            if cart_unit['goods_pk'] == goods_pk:
                cart_unit['quantity'] += quantity
                return cart_list

        cart_list.append(SessionCartManager._make_unit(goods_pk, quantity))
        return cart_list

    @staticmethod
    def minus_unit(cart_list, goods_pk):
        goods_pk = int(goods_pk)

        for cart_unit in cart_list:
            if cart_unit['quantity'] > 1 and cart_unit['goods_pk'] == goods_pk:
                cart_unit['quantity'] -= 1
                return cart_list

        return cart_list

    @staticmethod
    def delete_unit(cart_list, goods_pk):
        goods_pk = int(goods_pk)

        for cart_unit in cart_list:
            if cart_unit['goods_pk'] == goods_pk:
                cart_list.remove(cart_unit)

        return cart_list

    @staticmethod
    def rendering_unit(cart_list):
        return [
            {'goods': Goods.objects.get(pk=cart_unit['goods_pk']).name,
             'add_tax': Goods.objects.get(pk=cart_unit['goods_pk']).add_tax,
             'price': Goods.objects.get(pk=cart_unit['goods_pk']).add_tax * cart_unit['quantity'],
             'goods_pk': cart_unit['goods_pk'],
             'quantity': cart_unit['quantity']}
            for cart_unit in cart_list]

    @staticmethod
    def total_price(cart_list):
        total_cart = []
        for cart_unit in cart_list:
            price = Goods.objects.get(pk=cart_unit['goods_pk']).add_tax * cart_unit['quantity']
            total_cart.append(price)

        return sum(total_cart)
