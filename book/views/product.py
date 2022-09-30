from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

from ..models.product import Product
from ..serializers.product import ProductSerializer


class ProductsPagination(LimitOffsetPagination):
    '''Распил списка продуктов на куски по default_limit штук'''
    default_limit = 2
    max_limit = 30


class ProductListView(ListAPIView):
    """Поиск продуктов по номеру или части названия"""
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ProductsPagination

    def get_queryset(self):
        params = self.request.data

        # Если есть номер(-а), берём продукты по номерам
        if params.get('id'):
            if isinstance(params.get('id'), list):
                return Product.objects.filter(id__in=params.get('id'))
            else:
                return Product.objects.filter(id=params.get('id'))

        # Если номера нет, значит есть имя - ищем по части имени
        if params.get('name'):
            return Product.objects.filter(name__istartswith=params.get('name')).order_by('name')

        # Если нет ни того, ни другого
        return Product.objects.none()
