from django.urls import path, include
from .views import *
from rest_framework import routers

#Creamos las listas del API

router = routers.DefaultRouter()
router.register('productos', ProductoViewset)
router.register('tipoproductos', TipoProductoViewset)


urlpatterns = [
    #API
    path('api/', include(router.urls)),
    #RUTAS
    path('', index, name="index"),
    path('indexapi/', indexapi, name="indexapi"),
    path('about/', about, name="about"),
    path('blog/', blog, name="blog"),
    path('contact/', contact, name="contact"),
    path('detail/', detail, name="detail"),
    path('price/', price, name="price"),
    path('product/', product, name="product"),
    path('service/', service, name="service"),
    path('team/', team, name="team"),
    path('testimonial/', testimonial, name="testimonial"),
    path('rastreo/', rastreo, name="rastreo"), 
    path('pagocarro/', pagocarro, name="pagocarro"),
    
    #CRUD
    path('add/', add, name="add"),
    path('update/<id>/', update, name="update"),
    path('delete/<id>/', delete, name="delete"),
    #Carrito
    path('carrito/', carrito, name="carrito"),
    path('agregar_producto/<producto_id>/',agregar_producto, name="agregar_producto"),
    path('deleteCarrito/<item_id>/', deleteCarrito, name='deleteCarrito'),
    #REGISTRO
    path('registro/', registro, name="registro"),
    #Compra
    path('agregar_compra/', agregar_compra, name="agregar_compra"),

    
    path('lista_compras/', lista_compras, name='lista_compras'),
    #path('detalle_compra/<compra_id>/', detalle_compra, name='detalle_compra'),
    path('detalle_productos_compra/<compra_id>/productos/', detalle_productos_compra, name='detalle_productos_compra'),
]
