
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
    path ("bodeguero", render_views.bodeguero,name="bodeguero"),
    path('catalogo_bodeguero/', render_views.catalogo_bodeguero, name='catalogo_bodeguero'),
    path('producto/<int:id>/', render_views.detalle_producto, name='detalle_producto'),
    path('aumentar_stock/<int:id>/', render_views.aumentar_stock, name='aumentar_stock'),
    path('disminuir_stock/<int:id>/', render_views.disminuir_stock, name='disminuir_stock'),

    # Login views
    path ("login_user", user_views.login_user,name="login_user"),
    path ("logout_user", user_views.logout_user,name="logout_user"),
    path ("register_user", user_views.register_user,name="register_user"),
    path("registro_bodeguero/", user_views.registro_bodeguero, name="registro_bodeguero"),
    path ("login_bodeguero", user_views.login_bodeguero,name="login_bodeguero"),

    # Carrito views
    path ("add_to_cart/<int:id>", carrito_views.add_to_cart,name="add_to_cart"),
    path ("remove_from_cart/<int:id>", carrito_views.remove_from_cart,name="remove_from_cart"),
    path('pago/iniciar/', carrito_views.iniciar_pago, name='iniciar_pago'),
    path('pago/exito/', carrito_views.confirmar_pago, name='confirmar_pago'),
    path('convertir_dinero/', carrito_views.convertir_dinero, name='convertir_dinero'),
    path('clear_cart/', carrito_views.clear_cart, name='clear_cart'),
    path('pago_exito/',carrito_views.pago_exito, name='pago_exito'),
    
    
    
    
    
]
