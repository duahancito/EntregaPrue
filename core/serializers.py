#Nos va a permitir cenvertir la data

from .models import *
from rest_framework import serializers

class TipoProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoSerializers(serializers.ModelSerializer):
    tipo = TipoProductoSerializers(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'


class CompraSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Compra
        fields = '__all__'

class ProductoCompraSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductoCompra
        fields = '__all__'
