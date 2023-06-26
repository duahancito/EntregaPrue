from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Carrito, Producto, ItemCarrito
from django.contrib.auth.decorators import login_required, user_passes_test
from .serializers import *
from rest_framework import viewsets
import requests
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group


# FUNCION QUNERICA QUE VALIDA EL GRUPO DEL USUARIO
def grupo_requerido(nombre_grupo):
    def decorator(view_fuc):
        @user_passes_test(lambda user: user.groups.filter(name=nombre_grupo).exists())
        def wrapper(request, *arg, **kwargs):
            return view_fuc(request,  *arg, **kwargs)
        return wrapper
    return decorator

#@grupo_requerido('vendedor')
#CUENAOD CREAN EL USUARIO LO ASIGNA INMEDIATAMENTE AL GRUPO 
# grupo= group.abjects.get(name='cliente')
#user.groups.add(grupo)





#Nos permite mostrar la info
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    #queryset = Producto.objects.filter(tipo=1)
    serializer_class = ProductoSerializers

class TipoProductoViewset(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    #queryset = Producto.objects.filter(tipo=1)
    serializer_class = TipoProductoSerializers

def indexapi(request):
    #OBTIENE EL JSON DEL API/LOS DATOS DEL API
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api') 
    
    
    #TRANFORMAR EL JSON
    productos = respuesta.json()
    monedas = respuesta2.json()
    
   
 
    data = {
        'listado': productos,
        'monedas': monedas,
        
 
    }
    return render(request, 'core/indexapi.html', data)



def index(request):
    productosAll = Producto.objects.all() # SELECT * FROM producto
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    try:
        paginator = Paginator(productosAll, 4)
        productosAll = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productosAll,
        'paginator': paginator
    }
    return render(request, 'core/index.html', data)

def product(request):
    productosAll = Producto.objects.all() # SELECT * FROM producto
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    try:
        paginator = Paginator(productosAll, 8)
        productosAll = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productosAll,
        'paginator': paginator
    }
    return render(request, 'core/product.html', data)

# CRUD
@grupo_requerido('vendedor')
@login_required
def add(request):
    data = {
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            #data['msj'] = "Producto guardado correctamente"
            messages.success(request, "Producto almacenado correctamente")

    return render(request, 'core/add-product.html', data)

@grupo_requerido('vendedor')
@login_required
def update(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    data = {
        'form' : ProductoForm(instance=producto) # CARGAMOS EL PRODUCTO EN EL FORMULARIO
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES) # NUEVA INFORMACION
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            #data['msj'] = "Producto actualizado correctamente"
            messages.success(request, "Producto actualizado correctamente")
            data['form'] = formulario # CARGA LA NUEVA INFOR EN EL FORMULARIO

    return render(request, 'core/update-product.html', data)

@grupo_requerido('vendedor')
@login_required
def delete(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    producto.delete()

    return redirect(to="index")

def about(request):
    return render(request, 'core/about.html',)


def blog(request):
    return render(request, 'core/blog.html')


def contact(request):
    return render(request, 'core/contact.html')


def detail(request):
    return render(request, 'core/detail.html')




@login_required
def price(request):
    #OBTIENE EL JSON DEL API/LOS DATOS DEL API
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']
    #LOGICA DE SUMAR LOS PRECIOS DEL CARRITO
    valor_total = 20
    data = {
        'valor' : valor_total
    }
    return render(request, 'core/price.html',data)




def service(request):
    return render(request, 'core/service.html')


def team(request):
    return render(request, 'core/team.html')


def testimonial(request):
    return render(request, 'core/testimonial.html')



#Carrito
@grupo_requerido('cliente')
@login_required
def carrito(request):
    carrito = Carrito.objects.get(usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.subtotal() for item in items)
    productosAll = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = productosAll['serie'][0]['valor']
    valor_carrito = 20000
    valor_total = valor_carrito/valor_usd 
    data = {
        'valor' : round(valor_total, 2),
        'listado': productosAll,
        
    }
    return render(request, 'core/carrito.html', {'carrito': carrito, 'items': items, 'total': total})

@grupo_requerido('cliente')
def agregar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    carrito, created= Carrito.objects.get_or_create(usuario=request.user)
    item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)


    if not item_created:
        if producto.stock >= 1:
            item.cantidad += 1
            item.save()
            producto.stock -= 1
            producto.save()
            carrito.productos.add(producto)
        else:
            return redirect('carrito')
    else:
        if producto.stock >= 1:
            item.cantidad = 1
            item.save()
            producto.stock -= 1
            producto.save()
            carrito.productos.add(producto)
        else:
            return redirect('index')
    
    carrito.save()

    return redirect('carrito')

@grupo_requerido('cliente')
@login_required
def deleteCarrito(request, item_id):
    itemcarrito = ItemCarrito.objects.get(id=item_id)
    itemcarrito.delete()
    itemcarrito.producto.stock += itemcarrito.cantidad
    itemcarrito.producto.save()


    return redirect(to="carrito")

#Rastreo
@grupo_requerido('cliente')
def rastreo(request):
    carrito = Carrito.objects.get(usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.subtotal() for item in items)
    return render(request, 'core/rastreo.html', {'carrito': carrito, 'items': items, 'total': total})

#PagoCarro
@grupo_requerido('cliente')
def pagocarro(request):
    carrito = Carrito.objects.get(usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.subtotal() for item in items)
    respuesta = requests.get('https://mindicador.cl/api/dolar')
    monedas = respuesta.json()
    valor_usd = monedas['serie'][0]['valor']
    #LOGICA DE SUMAR LOS PRECIOS DEL CARRITO
    valor_carrito = total
    valor_total = valor_carrito/valor_usd 
    data = {
        'valor' : round(valor_total, 2),
        'listado': monedas,
        'carrito': carrito,
        'items': items,
        'total': total
        
    }
    return render(request, 'core/pagocarro.html', data)

#REGISTRO
def registro(request):
    data={
        'form': CustomUserCreationform()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationform(data=request.POST)
        if formulario.is_valid():
            user=formulario.save()
            user.groups.add(Group.objects.get(name='Cliente'))

            #redirigir al home 
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro Exitoso")
            return redirect(to="index")
        data["form"] = formulario


    return render(request, 'registration/registro.html', data)

@grupo_requerido('cliente')
def agregar_compra(request):
    carrito = Carrito.objects.get(usuario=request.user)
    compra = Compra(usuario=request.user, total=carrito.total)
    compra.save()
    items = ItemCarrito.objects.filter(carrito=carrito)

  
    for item in items:  
        producto_compra = ProductoCompra(compra=compra, producto=item.producto, cantidad=item.cantidad)
        producto_compra.save()
        item.delete()

    
    carrito.productos.clear()
    carrito.total = 0
    carrito.save()

    return redirect('lista_compras')

@grupo_requerido('cliente')
def lista_compras(request):
    compras = Compra.objects.filter(usuario=request.user)
    return render(request, 'core/lista_compras.html', {'compras': compras})

@grupo_requerido('cliente')
def detalle_productos_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    productos_compra = compra.productocompra_set.all()
    return render(request, 'core/detalle_productos_compra.html', {'compra': compra, 'productos_compra': productos_compra})
