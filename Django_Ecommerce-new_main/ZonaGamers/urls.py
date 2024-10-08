from django.urls import path
from .views import render_views, carrito_views, user_views

urlpatterns = [

    #  Render views
    path ("", render_views.home,name="home"),
    path ("about", render_views.about,name="about"),
    path ("carrito", render_views.carrito,name="carrito"),
    path('catalogo/', render_views.catalogo, name="catalogo"),
    path ("login", render_views.login,name="login"),
    path ("registro", render_views.registro,name="registro"),
    path ("producto_spiders", render_views.producto_spider,name="producto_spider"),
    path ("crud", render_views.crud,name="crud"), 

    # Login views
    path ("login_user", user_views.login_user,name="login_user"),
    path ("logout_user", user_views.logout_user,name="logout_user"),
    path ("register_user", user_views.register_user,name="register_user"),

    # Carrito views
    path ("add_to_cart/<int:id>", carrito_views.add_to_cart,name="add_to_cart"),
    path ("remove_from_cart/<int:id>", carrito_views.remove_from_cart,name="remove_from_cart"),
    path ("clear_cart/<int:cartId>", carrito_views.clear_cart,name="clear_cart"),
]
