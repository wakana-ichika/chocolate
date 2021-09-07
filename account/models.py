from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator
from django.db import models
from goods.models import Goods
from store.models import Cart
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    user_in_migrations = True

    def _create_user(self, name, email, password, **extra_fields):
        if not name:
            raise ValueError('User must have a username.')
        if not email:
            raise ValueError('User must have a email.')

        email = self.normalize_email(email)
        user = self.model(
             name=name, email=email, password=password, cart=Cart.objects.create(), **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=true.')

        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('ユーザーネーム', max_length=50, unique=True, blank=True, null=True)
    name = models.CharField('お名前', max_length=50, help_text='必須')
    furigana = models.CharField('フリガナ', max_length=50, help_text='必須')
    tell = models.CharField('お電話番号', max_length=13, blank=True, null=True)
    email = models.EmailField('メールアドレス', help_text='必須', unique=True)
    post_code = models.CharField('郵便番号', max_length=8, help_text='必須')
    address1 = models.CharField('都道府県', max_length=100, help_text='必須')
    address2 = models.CharField('市町村番地', max_length=100, help_text='必須')
    address3 = models.CharField('建物名（マンション・アパートなど）', max_length=100, blank=True, null=True)
    register_datetime = models.DateTimeField('登録日時', auto_now_add=True)
    is_staff = models.BooleanField('スタッフ', default=False)
    is_active = models.BooleanField('有効', default=True)
    cart = models.OneToOneField(to=Cart, verbose_name='カート', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()


class Shopping(models.Model):
    user_pk = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    goods_pk = models.ForeignKey(Goods, verbose_name='購入商品', on_delete=models.PROTECT)
    shopping_time = models.DateTimeField('購入時刻', default=timezone.now)
    how_many = models.PositiveIntegerField('購入数', validators=[MaxValueValidator(10)], blank=False)
    state_flag = models.BooleanField('運用状況', default=True)

    def __str__(self):
        return str(self.user_pk) + ':' + str(self.goods_pk)
