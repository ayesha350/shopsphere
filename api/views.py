from django.shortcuts import render
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.pagination import PageNumberPagination


@api_view(["GET"])
def home(request):
    return Response({
        "message": "Welcome to ShopSphere API"
    })


@api_view(["POST"])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "message": "User Registered Successfully"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
def category_list(request):

    if request.method == "GET":

        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def product_list(request):

    if request.method == "GET":

        products = Product.objects.all()

        search = request.GET.get("search")

        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        category = request.GET.get("category")

        if category:
            products = products.filter(category_id=category)

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":

        if not request.user.is_authenticated:
            return Response(
                {"message": "Login Required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.user.role != "seller":
            return Response(
                {"message": "Only sellers can add products"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(seller=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        ) 

        
        

@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):

    try:
        product = Product.objects.get(id=pk)

    except Product.DoesNotExist:
        return Response(
            {"error": "Product Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET - Anyone can view product

    if request.method == "GET":

        serializer = ProductSerializer(product)

        return Response(serializer.data)


    # PUT - Only seller + owner

    elif request.method == "PUT":

        if not request.user.is_authenticated:
            return Response(
                {"message": "Login Required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.user.role != "seller":
            return Response(
                {"message": "Only sellers can modify products"},
                status=status.HTTP_403_FORBIDDEN
            )

        if product.seller != request.user:
            return Response(
                {"message": "You are not the owner of this product"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # DELETE - Only seller + owner

    elif request.method == "DELETE":

        if not request.user.is_authenticated:
            return Response(
                {"message": "Login Required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.user.role != "seller":
            return Response(
                {"message": "Only sellers can delete products"},
                status=status.HTTP_403_FORBIDDEN
            )

        if product.seller != request.user:
            return Response(
                {"message": "You are not the owner of this product"},
                status=status.HTTP_403_FORBIDDEN
            )

        product.delete()

        return Response(
            {"message": "Product Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET"])
def me(request):

    if not request.user.is_authenticated:
        return Response(
            {"message": "Login Required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return Response({
        "id": request.user.id,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "phone_number": request.user.phone_number,
        "role": request.user.role
    })        


@api_view(["POST"])
def add_to_cart(request):

    if not request.user.is_authenticated:
        return Response(
            {"message": "Login Required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    product_id = request.data.get("product")
    quantity = request.data.get("quantity", 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"message": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += int(quantity)
    else:
        cart_item.quantity = int(quantity)

    cart_item.save()

    serializer = CartSerializer(cart_item)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@api_view(["GET", "PUT", "DELETE"])
def cart(request):

    if not request.user.is_authenticated:
        return Response(
            {"message": "Login Required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # GET - View Cart
    if request.method == "GET":

        cart_items = Cart.objects.filter(
            user=request.user
        )

        serializer = CartSerializer(
            cart_items,
            many=True
        )

        return Response(serializer.data)


    # PUT - Update Quantity
    elif request.method == "PUT":

        cart_id = request.data.get("cart_id")
        quantity = request.data.get("quantity")

        try:
            cart_item = Cart.objects.get(
                id=cart_id,
                user=request.user
            )
        except Cart.DoesNotExist:
            return Response(
                {"message": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not quantity or int(quantity) <= 0:
            return Response(
                {"message": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response(serializer.data)


    # DELETE - Remove Item
    elif request.method == "DELETE":

        cart_id = request.data.get("cart_id")

        try:
            cart_item = Cart.objects.get(
                id=cart_id,
                user=request.user
            )
        except Cart.DoesNotExist:
            return Response(
                {"message": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()

        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(["POST"])
def place_order(request):

    if not request.user.is_authenticated:
        return Response(
            {"message": "Login Required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Get user's cart
    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():
        return Response(
            {"message": "Cart is empty"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check stock
    for item in cart_items:

        if item.quantity > item.product.stock:

            return Response(
                {
                    "message": f"Only {item.product.stock} units available for {item.product.name}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # Calculate total amount
    total_amount = 0

    for item in cart_items:

        total_amount += (
            item.product.price * item.quantity
        )

    # Create Order
    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount
    )

    # Create Order Items + Reduce Stock
    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        # Reduce product stock
        item.product.stock -= item.quantity
        item.product.save()

    # Empty cart after successful order
    cart_items.delete()

    # Return order details
    serializer = OrderSerializer(order)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )
@api_view(["GET"])
def my_orders(request):

    if not request.user.is_authenticated:
        return Response(
            {"message": "Login Required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    serializer = OrderSerializer(
        orders,
        many=True
    )

    return Response(serializer.data)

@api_view(["GET"])
def order_detail(request, order_id):

    if not request.user.is_authenticated:
        return Response(
            {"message": "Login Required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        order = Order.objects.get(
            id=order_id,
            user=request.user
        )
    except Order.DoesNotExist:
        return Response(
            {"message": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = OrderSerializer(order)

    return Response(serializer.data)


@api_view(["PUT"])
def cancel_order(request, order_id):

    if not request.user.is_authenticated:
        return Response(
            {"message": "Login Required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        order = Order.objects.get(
            id=order_id,
            user=request.user
        )
    except Order.DoesNotExist:
        return Response(
            {"message": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if order.status in ["shipped", "delivered"]:
        return Response(
            {"message": "Order cannot be cancelled"},
            status=status.HTTP_400_BAD_REQUEST
        )

    order.status = "cancelled"
    order.save()

    return Response({
        "message": "Order cancelled successfully",
        "status": order.status
    })