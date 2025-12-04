# ================================
# IMPORTACIONES Y UTILIDADES
# ================================

from decimal import Decimal  # Para operaciones de dinero (precios y totales)
from django.shortcuts import render, redirect, get_object_or_404  # Renderiza templates, redirige y obtiene objetos o 404
from django.contrib.auth import login, logout  # Funciones de autenticación
from django.contrib.auth.decorators import login_required  # Decorador para proteger vistas
from django.contrib.auth.forms import AuthenticationForm  # Formulario de login por defecto de Django
from django.contrib import messages  # Mensajes flash para notificaciones al usuario
from django.utils import timezone  # Manejo de fechas y horas con zona horaria
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import RegistroForm, CuentaForm, ProveedorForm, ProductoForm, UsuarioForm, AgregarCreditoForm, DevolucionForm
from .models import Producto, Proveedor, Compra, Usuario

from django.contrib.auth.decorators import user_passes_test  # Decorador para permisos de superusuario
from django.views.decorators.csrf import csrf_exempt  # Permite deshabilitar CSRF en ciertas vistas

# ============================================
# Decorador para proteger vistas de superusuarios
# ============================================
def superuser_required(view_func):
    """
    Permite que solo superusuarios accedan a la vista.
    Redirige a login si el usuario no es superuser.
    """
    return user_passes_test(
        lambda u: u.is_superuser,
        login_url='/login/'
    )(view_func)

# =================================================
# PROVEEDOR CRUD
# =================================================

# Lista todos los proveedores
@superuser_required
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'App_GameVerse/CRUD/proveedor_list.html', {'proveedores': proveedores})

# Crear proveedor
@csrf_exempt  # Evita error CSRF (no recomendado en producción)
@superuser_required
def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor creado exitosamente.")
            return redirect('App_GameVerse:proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'App_GameVerse/CRUD/proveedor_form.html', {'form': form})

# Actualizar proveedor
@csrf_exempt
@superuser_required
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect('App_GameVerse:proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'App_GameVerse/CRUD/proveedor_form.html', {'form': form})

# Eliminar proveedor
@csrf_exempt
@superuser_required
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)

    if request.method == "POST":
        proveedor.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect('App_GameVerse:proveedor_list')

    return render(request, 'App_GameVerse/CRUD/proveedor_confirm_delete.html', {
        'proveedor': proveedor
    })

# =================================================
# PRODUCTO CRUD
# =================================================

# Lista todos los productos
@superuser_required
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'App_GameVerse/CRUD/producto_list.html', {'productos': productos})

# Crear producto
@csrf_exempt
@superuser_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('App_GameVerse:producto_list')
    else:
        form = ProductoForm()
    return render(request, 'App_GameVerse/CRUD/producto_form.html', {'form': form})

# Actualizar producto
@csrf_exempt
@superuser_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('App_GameVerse:producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'App_GameVerse/CRUD/producto_form.html', {'form': form})

# Eliminar producto
@csrf_exempt
@superuser_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('App_GameVerse:producto_list')

    return render(request, 'App_GameVerse/CRUD/producto_confirm_delete.html', {
        'producto': producto
    })

# =================================================
# USUARIO CRUD
# =================================================

# Lista todos los usuarios
@superuser_required
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'App_GameVerse/CRUD/usuario_list.html', {'usuarios': usuarios})

# Crear usuario
@csrf_exempt
@superuser_required
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('App_GameVerse:usuario_list')
    else:
        form = UsuarioForm()
    return render(request, 'App_GameVerse/CRUD/usuario_form.html', {'form': form})

# Actualizar usuario
@csrf_exempt
@superuser_required
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('App_GameVerse:usuario_list')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'App_GameVerse/CRUD/usuario_form.html', {'form': form})

# Eliminar usuario
@csrf_exempt
@superuser_required
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('App_GameVerse:usuario_list')

    return render(request, 'App_GameVerse/CRUD/usuario_confirm_delete.html', {
        'usuario': usuario
    })


# Página de inicio
def home(request):
    return render(request, 'App_GameVerse/index.html')

# Registro de usuarios
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('App_GameVerse:home')
    else:
        form = RegistroForm()
    return render(request, 'App_GameVerse/registro.html', {'form': form})

# Login de usuarios
def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Si es superusuario → redirige a CRUD
            if user.is_superuser:
                return redirect('App_GameVerse:usuario_list')

            # Si no es superusuario → home normal
            return redirect('App_GameVerse:home')

        # Si el formulario no es válido → mostrar mensaje
        return render(request, 'App_GameVerse/login.html', {'form': form, 'error': "Credenciales incorrectas"})

    # GET → mostrar formulario
    form = AuthenticationForm(request)
    return render(request, 'App_GameVerse/login.html', {'form': form})

# Logout de usuario
def logout_view(request):
    logout(request)
    return redirect('App_GameVerse:home')


# =============================================
# TIENDA (CON ESTADO DE CARRITO Y BIBLIOTECA)
# =============================================
def tienda(request):
    """
    Muestra todos los productos disponibles en la tienda.
    Indica si ya están en la biblioteca o carrito del usuario.
    """
    productos = Producto.objects.filter(disponible=True)

    if request.user.is_authenticated:
        usuario = request.user
        # IDs de productos en biblioteca y carrito del usuario
        biblioteca_ids = [p.get('id_producto') for p in usuario.biblioteca]
        carrito_ids = [c.get('id_producto') for c in usuario.carrito]

        # Marcar cada producto si ya está en biblioteca o carrito
        for p in productos:
            p.ya_en_biblioteca = p.id in biblioteca_ids
            p.ya_en_carrito = p.id in carrito_ids
    else:
        # Usuario no autenticado → no tiene productos
        for p in productos:
            p.ya_en_biblioteca = False
            p.ya_en_carrito = False

    return render(request, 'App_GameVerse/tienda.html', {'productos': productos})


# =============================================
# DETALLE PRODUCTO (CON ESTADOS)
# =============================================
def producto_detalle(request, pk):
    """
    Vista del detalle de un producto individual.
    Muestra si ya está en biblioteca o carrito.
    """
    producto = get_object_or_404(Producto, pk=pk)

    if request.user.is_authenticated:
        usuario = request.user
        biblioteca_ids = [p.get('id_producto') for p in usuario.biblioteca]
        carrito_ids = [c.get('id_producto') for c in usuario.carrito]

        producto.ya_en_biblioteca = producto.id in biblioteca_ids
        producto.ya_en_carrito = producto.id in carrito_ids
    else:
        producto.ya_en_biblioteca = False
        producto.ya_en_carrito = False

    return render(request, 'App_GameVerse/detalle_producto.html', {'producto': producto})

# =======================================================
# CARRITO (almacenado en usuario.carrito)
# =======================================================

@login_required
def agregar_al_carrito(request, pk):
    """
    Agrega un producto al carrito del usuario.
    Verifica si ya está en biblioteca o carrito.
    """
    producto = get_object_or_404(Producto, pk=pk)
    usuario = request.user

    biblioteca = usuario.biblioteca or []
    carrito = usuario.carrito or []

    # Producto ya en biblioteca
    if any(item.get('id_producto') == producto.id for item in biblioteca):
        messages.warning(request, "Ya tienes este producto en tu biblioteca.")
        return redirect('App_GameVerse:producto_detalle', pk=pk)

    # Producto ya en carrito
    if any(item.get('id_producto') == producto.id for item in carrito):
        messages.info(request, "Este producto ya está en tu carrito.")
    else:
        carrito.append({
            'id_producto': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio)
        })
        usuario.carrito = carrito
        usuario.save()
        messages.success(request, f"{producto.nombre} ha sido agregado al carrito.")

    return redirect('App_GameVerse:carrito_view')


@login_required
def carrito_view(request):
    """
    Vista del carrito del usuario.
    Calcula subtotal, IVA y total.
    """
    usuario = request.user
    carrito = usuario.carrito or []

    items = []
    subtotal = Decimal('0.00')

    for entry in carrito:
        pid = entry.get('id_producto')
        if not pid:
            continue

        producto = get_object_or_404(Producto, pk=pid)

        # precio en carrito, o precio del producto
        price = Decimal(str(entry.get('precio', producto.precio)))

        items.append({
            'id_producto': producto.id,
            'producto': producto,
            'precio': price,
            'subtotal': price
        })

        subtotal += price

    # -------------------------
    #        IVA 16%
    # -------------------------
    iva = subtotal * Decimal("0.16")
    total_con_iva = subtotal + iva

    return render(request, 'App_GameVerse/carrito.html', {
        'items': items,
        'subtotal': subtotal,
        'iva': iva,
        'total': total_con_iva       # importante: tu plantilla usa "total"
    })



@login_required
def eliminar_del_carrito(request, item_id):
    """
    Elimina un producto del carrito del usuario.
    """
    usuario = request.user
    carrito = usuario.carrito or []

    item_id = int(item_id)
    # Filtra todos los productos excepto el que se elimina
    nuevo_carrito = [entry for entry in carrito if entry.get('id_producto') != item_id]

    usuario.carrito = nuevo_carrito
    usuario.save()

    messages.success(request, "Producto eliminado del carrito.")
    return redirect('App_GameVerse:carrito_view')

@login_required
def comprar_carrito(request):
    """
    Procesa la compra de todos los productos en el carrito.
    Permite pagar con Tarjeta, Crédito o Efectivo.
    """
    usuario = request.user
    carrito = usuario.carrito or []

    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('App_GameVerse:carrito_view')

    subtotal = sum(Decimal(str(item.get('precio', 0))) for item in carrito)
    iva = subtotal * Decimal("0.16")
    total = subtotal + iva

    from .forms import MetodoPagoForm

    if request.method == 'POST':
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            metodo_pago = form.cleaned_data['metodo_pago']
            request.session['metodo_pago'] = metodo_pago
            request.session['total_carrito'] = str(total)

            biblioteca = usuario.biblioteca or []
            detalles = []

            # PAGO CON TARJETA → redirige a la vista de pago con tarjeta
            if metodo_pago == "Tarjeta":
                return redirect('App_GameVerse:comprar_carrito_tarjeta')

            # PAGO CON CRÉDITO
            elif metodo_pago == "Credito":
                if usuario.credito < total:
                    messages.error(request, "No tienes suficiente crédito para realizar esta compra.")
                    return redirect('App_GameVerse:carrito_view')

                usuario.credito -= total

                for entry in carrito:
                    pid = entry.get('id_producto')
                    if not pid:
                        continue
                    producto = get_object_or_404(Producto, pk=pid)
                    if any(p.get('id_producto') == producto.id for p in biblioteca):
                        continue
                    detalles.append({'id_producto': producto.id, 'nombre': producto.nombre})
                    biblioteca.append({
                        'id_producto': producto.id,
                        'nombre': producto.nombre,
                        'fecha_compra': timezone.now().strftime('%Y-%m-%d %H:%M')
                    })

                if detalles:
                    Compra.objects.create(
                        usuario=usuario,
                        detalles_productos=detalles,
                        total=total,
                        metodo_pago="Credito",
                        estatus="Completada"
                    )
                    usuario.biblioteca = biblioteca
                    usuario.carrito = []
                    usuario.save()
                    messages.success(request, "Compra realizada con crédito.")
                else:
                    messages.warning(request, "Todos los productos del carrito ya están en tu biblioteca.")

                return redirect('App_GameVerse:biblioteca')

            # PAGO CON EFECTIVO
            elif metodo_pago == "Efectivo":
                for entry in carrito:
                    pid = entry.get('id_producto')
                    if not pid:
                        continue
                    producto = get_object_or_404(Producto, pk=pid)
                    if any(p.get('id_producto') == producto.id for p in biblioteca):
                        continue
                    detalles.append({'id_producto': producto.id, 'nombre': producto.nombre})
                    biblioteca.append({
                        'id_producto': producto.id,
                        'nombre': producto.nombre,
                        'fecha_compra': timezone.now().strftime('%Y-%m-%d %H:%M')
                    })

                if detalles:
                    Compra.objects.create(
                        usuario=usuario,
                        detalles_productos=detalles,
                        total=total,
                        metodo_pago="Efectivo",
                        estatus="Completada"
                    )
                    usuario.biblioteca = biblioteca
                    usuario.carrito = []
                    usuario.save()
                    messages.success(request, "Has comprado todos los productos del carrito con efectivo.")
                else:
                    messages.warning(request, "Todos los productos del carrito ya están en tu biblioteca.")

                return redirect('App_GameVerse:biblioteca')

    else:
        form = MetodoPagoForm()

    return render(request, 'App_GameVerse/seleccionar_metodo_pago.html', {
        'form': form,
        'total': total
    })

@login_required
def pago_tarjeta(request):
    """
    Procesa la compra del carrito mediante tarjeta (simulado).
    """
    usuario = request.user
    carrito = usuario.carrito or []

    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('App_GameVerse:carrito_view')

    total = sum(Decimal(str(item.get('precio', 0))) for item in carrito)

    from .forms import PagoTarjetaForm

    if request.method == 'POST':
        form = PagoTarjetaForm(request.POST)
        if form.is_valid():
            biblioteca = usuario.biblioteca or []
            detalles = []

            for entry in carrito:
                pid = entry.get('id_producto')
                if not pid:
                    continue
                producto = get_object_or_404(Producto, pk=pid)
                if any(p.get('id_producto') == producto.id for p in biblioteca):
                    continue
                detalles.append({'id_producto': producto.id, 'nombre': producto.nombre})
                biblioteca.append({
                    'id_producto': producto.id,
                    'nombre': producto.nombre,
                    'fecha_compra': timezone.now().strftime('%Y-%m-%d %H:%M')
                })

            if detalles:
                Compra.objects.create(
                    usuario=usuario,
                    detalles_productos=detalles,
                    total=total,
                    metodo_pago="Tarjeta",
                    estatus="Completada"
                )
                usuario.biblioteca = biblioteca
                usuario.carrito = []
                usuario.save()
                messages.success(request, "Has comprado todos los productos del carrito con tarjeta.")
            else:
                messages.warning(request, "Todos los productos del carrito ya están en tu biblioteca.")

            return redirect('App_GameVerse:biblioteca')
    else:
        form = PagoTarjetaForm()

    return render(request, 'App_GameVerse/pago_tarjeta.html', {
        'form': form,
        'total': total
    })

# Detalle de un proveedor y sus productos
def proveedor_detalle(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    productos = proveedor.productos.filter(disponible=True)
    return render(request, 'App_GameVerse/proveedor.html', {
        'proveedor': proveedor,
        'productos': productos
    })

# Vista de la biblioteca del usuario
@login_required
def biblioteca_view(request):
    user = request.user

    biblioteca = user.biblioteca or []
    productos = []

    for item in biblioteca:
        id_prod = item.get("id_producto")
        if not id_prod:
            continue

        try:
            producto = Producto.objects.get(pk=id_prod)
            productos.append({
                "producto": producto,
                "fecha_compra": item.get("fecha_compra"),
            })
        except Producto.DoesNotExist:
            continue

    return render(request, "App_GameVerse/biblioteca.html", {
        "productos": productos
    })

# Historial de compras del usuario
@login_required
def compras_view(request):
    usuario = request.user
    compras = Compra.objects.filter(usuario=usuario).order_by('-fecha_compra')
    return render(request, 'App_GameVerse/compras.html', {'compras': compras})

@login_required
def cuenta(request):
    """
    Permite al usuario actualizar o eliminar su cuenta.
    """
    usuario = request.user

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            usuario.delete()
            messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
            return redirect('App_GameVerse:home')

        form = CuentaForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu cuenta ha sido actualizada correctamente.")
            return redirect('App_GameVerse:cuenta')
    else:
        form = CuentaForm(instance=usuario)

    return render(request, 'App_GameVerse/cuenta.html', {'form': form})

# ===============================
# FUNCIONES WRAPPER PARA URLS
# ===============================
@login_required
def comprar_carrito_efectivo(request):
    # Redirige a comprar_carrito con método Efectivo
    return comprar_carrito(request)

@login_required
def comprar_carrito_tarjeta(request):
    # Redirige a pago_tarjeta
    return pago_tarjeta(request)

# =================================================
# FUNCIONES DEL CREDITO
# =================================================
@login_required
def credito(request):
    """
    Permite agregar crédito al usuario desde un formulario.
    """
    if request.method == "POST":
        form = AgregarCreditoForm(request.POST)
        if form.is_valid():
            monto = form.cleaned_data['credito']
            usuario = request.user
            usuario.credito += Decimal(monto)
            usuario.save()
            messages.success(request, f"Se han agregado ${monto} a tu crédito.")
            return redirect("App_GameVerse:tienda")
    else:
        form = AgregarCreditoForm()

    return render(request, "App_GameVerse/credito.html", {"form": form})

@login_required
def devolver_producto(request, producto_id):
    user = request.user

    producto = get_object_or_404(Producto, pk=producto_id)

    # Validar que el producto esté en la biblioteca
    biblioteca = user.biblioteca or []
    entrada = next((item for item in biblioteca if item["id_producto"] == producto_id), None)

    if not entrada:
        return render(request, "App_GameVerse/error.html", {
            "mensaje": "Este producto no está en tu biblioteca."
        })

    if request.method == "POST":
        metodo = request.POST.get("metodo")

        # Eliminar de la biblioteca
        nueva_biblio = [item for item in biblioteca if item["id_producto"] != producto_id]
        user.biblioteca = nueva_biblio

        # Reembolso como crédito
        if metodo == "credito":
            user.credito += producto.precio
            user.save()
            return redirect("App_GameVerse:biblioteca")

        # Reembolso a tarjeta
        elif metodo == "tarjeta":
            numero = request.POST.get("numero_tarjeta")
            banco = request.POST.get("banco")
            titular = request.POST.get("nombre_titular")

            # Aquí NO hacemos transacciones reales.
            # Solo simularíamos que se enviará un depósito.
            user.save()
            return redirect("App_GameVerse:biblioteca")

    return render(request, "App_GameVerse/devolver_producto.html", {
        "producto": producto
    })


@login_required
def cambiar_contrasena(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener sesión después de cambiar contraseña
            messages.success(request, "Tu contraseña se ha actualizado correctamente.")
            return redirect("App_GameVerse:cuenta")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "App_GameVerse/cambiar_contrasena.html", {"form": form})