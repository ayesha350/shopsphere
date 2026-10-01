from rest_framework import serializers
from .models import *



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password"
        ]

    def create(self, validated_data):

        return MyUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"]
        )



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"





class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"           

class CartSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "created_at"
        ]


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price"
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "total_amount",
            "status",
            "items",
            "created_at"
        ]                