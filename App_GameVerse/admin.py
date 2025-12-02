from django.contrib import admin
from .models import Usuario, Producto, Proveedor, Compra


# ==========================
#  USUARIO
# ==========================
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fecha_nacimiento', 'pais', 'estatus', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('estatus', 'is_active', 'pais')
    ordering = ('username',)  # Orden alfabético por username


# ==========================
#  PRODUCTO
# ==========================
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio', 'proveedor', 'disponible')
    list_filter = ('tipo', 'disponible', 'proveedor')
    search_fields = ('nombre', 'genero')
    ordering = ('nombre',)


# ==========================
#  PROVEEDOR
# ==========================
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'pais', 'sitio_web', 'estatus')
    search_fields = ('nombre', 'pais')
    list_filter = ('tipo', 'estatus')
    ordering = ('nombre',)


# ==========================
#  COMPRA
# ==========================
@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_productos', 'total', 'metodo_pago', 'estatus', 'fecha_compra')
    list_filter = ('estatus', 'metodo_pago', 'fecha_compra')
    search_fields = ('usuario__username',)
    ordering = ('-fecha_compra',)  # Últimas compras primero

    def get_productos(self, obj):
        """
        Muestra los nombres de los productos de la compra en una sola cadena separada por comas.
        """
        try:
            productos = [p.get('nombre', 'Sin nombre') for p in obj.detalles_productos]
            return ", ".join(productos) if productos else "Sin productos"
        except Exception:
            return "Error al leer productos"

    get_productos.short_description = 'Productos'  # Nombre de columna en admin
