from django.db import models
from django.core.validators import MinValueValidator
from goods.models import Goods

# Create your models here.


class CartUnit(models.Model):
    goods = models.ForeignKey(Goods, verbose_name='商品名', on_delete=models.CASCADE, blank=False)
    quantity = models.PositiveIntegerField('購入数', blank=False, validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return '{}:{}'.format(self.goods.name, self.quantity)


class Cart(models.Model):
    units = models.ManyToManyField(to=CartUnit, verbose_name='カートユニット', blank=True)

    def small(self):

        return [unit.goods.add_tax * unit.quantity for unit in self.units.all()]

    def total_price(self):
        total_price = [unit.goods.add_tax * unit.quantity for unit in self.units.all()]
        return sum(total_price)

    def add_unit(self, unit_add):
        if unit_add.goods in [unit.goods for unit in self.units.all()]:
            unit_origin = self.units.get(goods_id=unit_add.goods.id)
            unit_origin.quantity += unit_add.quantity
            unit_origin.save()
        else:
            unit_add.save()
            self.units.add(unit_add)

    def minus_unit(self, unit_add):
        if unit_add.goods in [unit.goods for unit in self.units.all()]:
            unit_origin = self.units.get(goods_id=unit_add.goods.id)
            if unit_origin.quantity > 1:
                unit_origin.quantity -= unit_add.quantity
                unit_origin.save()

    def _add_section_unit(self, goods_pk, quantity):
        goods_pk = int(goods_pk)

        if goods_pk in [unit.goods.pk for unit in self.units.all()]:
            unit_origin = self.units.get(goods_id=goods_pk)
            unit_origin.quantity += quantity
            unit_origin.save()
        else:
            unit_add = CartUnit(goods=Goods.objects.get(pk=goods_pk), quantity=quantity)
            unit_add.save()
            self.units.add(unit_add)

    def import_session(self, session_cart):
        for cart_unit in session_cart:
            self._add_section_unit(cart_unit['goods_pk'], cart_unit['quantity'])

    def __str__(self):
        return "{}様のシッピングカートです。".format(self.user.email)
