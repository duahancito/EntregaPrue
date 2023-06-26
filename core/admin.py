from django.contrib import admin
from .models import *
# Register your models here.


# DEJA EN MODO TABLA LA VISUALIZACION EN EL ADMIN
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo','vigente']
    search_fields = ['nombre']

class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['id','producto','cantidad']

class CompraAdmin(admin.ModelAdmin):
    list_display = ['id']

class ProductocompraAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(TipoProducto)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Carrito)
admin.site.register(ItemCarrito, ItemCarritoAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(ProductoCompra, ProductocompraAdmin)
