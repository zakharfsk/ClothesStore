import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_price_id = models.CharField(max_length=256, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'

    def __str__(self):
        return f'Продукт: {self.name} | Категорія: {self.category.name}'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.stripe_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_price_id = stripe_product_price['id']

        super(Product, self).save(force_insert,
                                  force_update,
                                  using,
                                  update_fields)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(
            name=self.name,
            description=self.description,
        )
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=int(self.price * 100),
            currency='uah',
        )

        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum([basket.sum() for basket in self])

    def total_quantity(self):
        return sum([basket.quantity for basket in self])

    def stripe_products(self):
        return [{'price': basket.product.stripe_price_id, 'quantity': basket.quantity} for basket in self]


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Користувач: {self.user.username} | Продукт: {self.product.name} | Кількість: {self.quantity}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        return {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }

    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            return obj, True
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            return basket, False
