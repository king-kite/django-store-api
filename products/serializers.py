from rest_framework import serializers
from .models import Product, ProductImage, Review


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_images')

    class Meta:
        model = ProductImage
        fields = ('image', 'main')

    def get_images(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_product_images')

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'description', 'price', 'discount_price', 'images')

    def get_product_images(self, obj):
        request = self.context.get('request')
        images = obj.image.all()
        serializer = ProductImageSerializer(images, many=True, context={'request': request})
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
