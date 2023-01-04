from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer


class ProductListView(APIView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductDetailView(APIView):

    def get_object(self, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)
            return product
        except Product.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        product = self.get_object(kwargs['slug'])
        if product:
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ReviewListView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_objects(self, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)
            reviews = product.product_reviews.all()
            return reviews
        except Product.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        reviews = self.get_objects(kwargs['slug'])
        if reviews:
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        if self.request.user.id == int(request.data['author']):
            serializer = ReviewSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ReviewDetailView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_object(self, pk):
        try:
            review = Review.objects.get(pk=pk)
            if review.product.is_active == True:
                return review
            return None
        except Review.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        review = self.get_object(kwargs['pk'])
        if review:
            if request.user == review.author:
                serializer = ReviewSerializer(review)
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        review = self.get_object(kwargs['pk'])
        user = request.user
        if review:
            if request.user == review.author and request.user.id == int(request.data['author']):
                serializer = ReviewSerializer(review, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        review = self.get_object(kwargs['pk'])
        if review:
            if request.user == review.author:
                review.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_404_NOT_FOUND)
