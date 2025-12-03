from django.urls import path                     # Importa la función para definir rutas URL
from . import views                              # Importa las vistas del módulo actual

app_name = 'App_GameVerse'                       # Nombre del "namespace" para evitar conflictos de rutas

urlpatterns = [
    path('', views.home, name='home'),           # Página principal (Home)

    # ---- AUTENTICACIÓN ----
    path('register/', views.register_view, name='register'),   # Ruta para registrar un nuevo usuario
    path('login/', views.login_view, name='login'),            # Ruta de inicio de sesión
    path('logout/', views.logout_view, name='logout'),         # Cerrar sesión del usuario autenticado

    # ---- TIENDA ----
    path('tienda/', views.tienda, name='tienda'),                      # Vista principal de la tienda de productos
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),  # Detalles de un producto por ID
    
    # ---- CARRITO ----
    path('producto/<int:pk>/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),  # Agregar producto al carrito
    path('carrito/', views.carrito_view, name='carrito_view'),                                  # Mostrar contenido del carrito
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),  # Eliminar un ítem por ID
    path('carrito/comprar/', views.comprar_carrito, name='comprar_carrito'),                    # Proceso inicial de compra
    path('carrito/pago_tarjeta/', views.pago_tarjeta, name='pago_tarjeta'),                    # Formulario de pago con tarjeta
    path('carrito/comprar_efectivo/', views.comprar_carrito_efectivo, name='comprar_carrito_efectivo'),  # Compra usando efectivo
    path('carrito/comprar_tarjeta/', views.comprar_carrito_tarjeta, name='comprar_carrito_tarjeta'),      # Finalizar compra con tarjeta

    # ---- PROVEEDORES ----
    path('proveedor/<int:pk>/', views.proveedor_detalle, name='proveedor_detalle'),  # Página con información del proveedor

    # ---- USUARIO ----
    path('biblioteca/', views.biblioteca_view, name='biblioteca'),      # Biblioteca del usuario (sus compras)
    path('compras/', views.compras_view, name='compras'),               # Historial de compras del usuario
    path("credito/", views.credito, name="credito"),                    # Página para gestionar o recargar crédito
    path("biblioteca/devolver/<int:producto_id>/", views.devolver_producto, name="devolver_producto"), # Devolver un producto comprado
    path('cuenta/', views.cuenta, name='cuenta'),                       # Configuración de cuenta del usuario

    # ---- CRUD PROVEEDOR ----
    path('crud/proveedores/', views.proveedor_list, name='proveedor_list'),              # Lista de proveedores
    path('crud/proveedores/crear/', views.proveedor_create, name='proveedor_create'),    # Crear proveedor
    path('crud/proveedores/editar/<int:pk>/', views.proveedor_update, name='proveedor_update'),  # Editar proveedor existente
    path('crud/proveedores/eliminar/<int:pk>/', views.proveedor_delete, name='proveedor_delete'),  # Eliminar proveedor

    # ---- CRUD PRODUCTO ----
    path('crud/productos/', views.producto_list, name='producto_list'),                  # Lista de productos
    path('crud/productos/crear/', views.producto_create, name='producto_create'),        # Crear nuevo producto
    path('crud/productos/editar/<int:pk>/', views.producto_update, name='producto_update'),  # Editar producto
    path('crud/productos/eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),  # Eliminar producto

    # ---- CRUD USUARIO ----
    path('crud/usuarios/', views.usuario_list, name='usuario_list'),                    # Lista de usuarios
    path('crud/usuarios/crear/', views.usuario_create, name='usuario_create'),          # Crear usuario desde panel admin
    path('crud/usuarios/editar/<int:pk>/', views.usuario_update, name='usuario_update'), # Editar usuario existente
    path('crud/usuarios/eliminar/<int:pk>/', views.usuario_delete, name='usuario_delete'), # Eliminar usuario
]
