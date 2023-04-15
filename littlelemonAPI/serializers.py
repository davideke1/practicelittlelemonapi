from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import MenuItem, Category, FoodItem, Rating
from rest_framework import serializers
import bleach


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class MenuSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory', 'category', 'category_id']


# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source='inventory')
#     price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     category = serializers.HyperlinkedRelatedField(
#         queryset= Category.objects.all(),
#         view_name='category-detail'
#     )
#
#     class Meta:
#         model = MenuItem
#         fields = ['id', 'title', 'price', 'stock','price_after_tax' , 'category']
#         # depth = 1
#     def calculate_tax(self, product:MenuItem):
#         return product.price * Decimal(1.1)


class MenuItemsSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=MenuItem.objects.all())])
    price = serializers.DecimalField(decimal_places=2, max_digits=5)


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category= CategorySerializer

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


class FoodItemSerializer(serializers.ModelSerializer):

    # def validate_title(self,value):
    #     return bleach.clean(value)
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        return super().validate(attrs)

    class Meta:
        model = FoodItem
        fields = "__all__"
        extra_kwargs = {
            'price': {'min_value': 2},
            'inventory': {'min_value': 0},
            'title': {
                'validators': [
                    UniqueValidator(queryset=FoodItem.objects.all())
                ]
            }
        }

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = Rating
        fields = ['user','menuitem_id','rating']

        validators = [
            UniqueTogetherValidator(
                queryset=Rating.objects.all(),
                fields=['user', 'menuitem_id']
            )
        ]

        extra_kwargs = {
            'rating': {'min_value': 0, 'max_value': 5},
        }
