from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

# ES DONDE CREAN LAS TABLAS
class TipoProducto(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=250)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)   
    imagen = models.ImageField(null=True,blank=True)
    vigente = models.BooleanField()

    def __str__(self):
        return self.nombre

#Carrito
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')
    total = models.PositiveIntegerField( default=0)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad 


#compras
class Compra(models.Model):
    ESTADOS =(
        ('Validacion','Validacion'),
        ('Preparacion','Preparacion'),
        ('Reparto','Reparto'),
        ('Entregado','Entregado'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS,default='validacion')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Compra {self.id}"

class ProductoCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"ProductoCompra {self.id}"