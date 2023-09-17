from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from products.models import Basket, Product
from products.serializers import BasketSerializer, ProductSerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = (IsAdminUser, )
        return super(ProductModelViewSet, self).get_permissions()


class BasketModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if product_id is None:
            return Response({'error': 'Product id is required'}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(id=product_id)

        if not products.exists():
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        basket, created = Basket.create_or_update(user=request.user, product_id=products.first().id)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        serializer = self.get_serializer(basket)

        return Response(serializer.data, status=status_code)
