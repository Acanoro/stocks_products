from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)

        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        instance.positions.all().delete()

        for position_data in positions_data:
            StockProduct.objects.create(stock=instance, **position_data)

        return instance
