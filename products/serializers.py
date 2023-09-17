from rest_framework import fields, serializers

from .models import Basket, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    def get_total_sum(self, obj):
        return Basket.objects.filter(user=obj.user).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user=obj.user).total_quantity()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'created_timestamp', 'sum', 'total_sum')
        read_only_fields = ('created_timestamp', )
