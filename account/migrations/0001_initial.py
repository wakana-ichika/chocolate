# Generated by Django 3.1.7 on 2021-03-13 10:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='ユーザーネーム')),
                ('name', models.CharField(help_text='必須', max_length=50, verbose_name='お名前')),
                ('furigana', models.CharField(help_text='必須', max_length=50, verbose_name='フリガナ')),
                ('tell', models.CharField(blank=True, max_length=13, null=True, verbose_name='お電話番号')),
                ('email', models.EmailField(help_text='必須', max_length=254, verbose_name='メールアドレス')),
                ('post_code', models.CharField(help_text='必須', max_length=8, verbose_name='郵便番号')),
                ('address1', models.CharField(help_text='必須', max_length=100, verbose_name='都道府県')),
                ('address2', models.CharField(help_text='必須', max_length=100, verbose_name='市町村番地')),
                ('address3', models.CharField(blank=True, max_length=100, null=True, verbose_name='建物名（マンション・アパートなど）')),
                ('register_datetime', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('is_staff', models.BooleanField(default=False, verbose_name='スタッフ')),
                ('is_active', models.BooleanField(default=True, verbose_name='有効')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopping_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='購入時刻')),
                ('how_many', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='購入数')),
                ('state_flag', models.BooleanField(default=True, verbose_name='運用状況')),
                ('goods_pk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.goods', verbose_name='購入商品')),
                ('user_pk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]