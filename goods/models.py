from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.


class GoodsGroup(models.Model):
    name = models.CharField('商品カテゴリ', unique=True, max_length=100, null=True)

    def __str__(self):
        return self.name


class Goods(models.Model):
    name = models.CharField('商品名', unique=True, max_length=100)
    management_code = models.CharField('管理コード', unique=True, max_length=100)
    price = models.PositiveIntegerField('本体価格', validators=[MaxValueValidator(100000)])
    add_tax = models.PositiveIntegerField('税込価格', validators=[MaxValueValidator(100000)])
    release_data = models.DateField('発売日', blank=True, null=True)
    release_flag = models.BooleanField('発売済み', default=False)
    text = models.TextField('説明', max_length=100000)
    image = models.ImageField('画像', null=True, upload_to='goods')
    state_flag = models.BooleanField('運用状況', default=True)
    group = models.ForeignKey(GoodsGroup, on_delete=models.CASCADE, verbose_name='商品カテゴリ')

    def save(self, *args, **kwargs):
        tax = self.price * 0.08
        self.add_tax = self.price + tax
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


