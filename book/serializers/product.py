from rest_framework import serializers

from ..models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продуктов"""

    name = serializers.CharField(max_length=255, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name']

    def validate_name(self, name):
        if name:
            if not Product.objects.filter(name=name).exists():
                raise serializers.ValidationError('Продукта под названием "{}" не найдено.'.format(name))
        return name

    def validate_id(self, id):
        if not Product.objects.filter(id=id).exists():
            raise serializers.ValidationError('Продукта под номером {} не найдено.'.format(id))
