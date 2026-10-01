from django.urls import path
from .views import *


urlpatterns = [
    path("", home),
    path("register/", register),
    path("categories/", category_list),
    path("products/", product_list),
    path("products/<int:pk>/", product_detail),
    path("me/", me),
    path("cart/add/", add_to_cart),
    path("cart/", cart),

    path("orders/place/", place_order),
    
    path("orders/", my_orders),
    path(
    "orders/<int:order_id>/",
    order_detail
    ),
    path(
    "orders/<int:order_id>/cancel/",
    cancel_order
    ),


]