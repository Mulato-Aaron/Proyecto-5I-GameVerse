from django.db import models                  # Importa las herramientas para definir modelos de Django
from django.contrib.auth.models import AbstractUser  # Permite extender el modelo de usuario base
from django.core.validators import MinValueValidator  # Validador para asegurar mínimos en campos numéricos
from decimal import Decimal                   # Permite manejar cantidades monetarias con precisión

# ==========================
#  MODELO: PROVEEDOR
# ==========================
class Proveedor(models.Model):                # Modelo que representa un proveedor de productos (juegos, DLC, etc.)
    TIPO_PROVEEDOR = [                        # Opciones válidas para clasificar al proveedor
        ('Desarrollador', 'Desarrollador'),
        ('Publisher', 'Publisher'),
    ]

    nombre = models.CharField(max_length=100)       # Nombre del proveedor
    tipo = models.CharField(max_length=20, choices=TIPO_PROVEEDOR)  # Tipo: desarrollador o publisher
    pais = models.CharField(max_length=50)          # País de origen del proveedor
    sitio_web = models.URLField(max_length=200, blank=True, null=True)  # Página web opcional del proveedor
    descripcion = models.TextField(blank=True, null=True)              # Información adicional opcional
    estatus = models.BooleanField(default=True)     # Indica si el proveedor está activo

    def __str__(self):                              # Representación legible del objeto
        return self.nombre


# ==========================
#  MODELO: PRODUCTO
# ==========================
class Producto(models.Model):                # Modelo que representa videojuegos, DLC y membresías
    TIPO_PRODUCTO = [                        # Tipos de productos permitidos
        ('Juego', 'Juego'),
        ('DLC', 'DLC'),
        ('Membresía', 'Membresía'),
    ]

    nombre = models.CharField(max_length=100)        # Nombre del producto
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO)  # Tipo de producto
    genero = models.CharField(max_length=50)         # Género del videojuego (acción, RPG, etc.)
    descripcion = models.TextField()                 # Descripción general del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio con precisión monetaria
    fecha_lanzamiento = models.DateField()           # Fecha oficial de lanzamiento del producto
    proveedor = models.ForeignKey(                   # Relación con el proveedor
        Proveedor,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    calificacion_promedio = models.DecimalField(     # Calificación promedio del producto
        max_digits=3, decimal_places=2, default=0
    )
    disponible = models.BooleanField(default=True)   # Indica si está visible para venta
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Imagen del producto

    def __str__(self):
        return self.nombre


# ==========================
#  MODELO: USUARIO
# ==========================
class Usuario(AbstractUser):                        # Extiende el modelo de usuario estándar de Django
    fecha_nacimiento = models.DateField(blank=True, null=True)  # Fecha de nacimiento opcional
    pais = models.CharField(max_length=50, blank=True, null=True)  # País opcional del usuario

    ESTATUS_CHOICES = [                             # Estados permitidos del usuario
        ('Activo', 'Activo'),
        ('No activo', 'No activo'),
    ]

    estatus = models.CharField(                     # Estado actual del usuario
        max_length=10,
        choices=ESTATUS_CHOICES,
        default='Activo'
    )
    biblioteca = models.JSONField(default=list, blank=True)  # Lista JSON de productos comprados
    carrito = models.JSONField(default=list, blank=True)     # Lista JSON del carrito de compras
    credito = models.DecimalField(                          # Dinero disponible para usar
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0.00)]                 # Evita valores negativos
    )

    def __str__(self):
        return self.username                              # Representa el usuario por su nombre de cuenta


# ==========================
#  MODELO: COMPRA
# ==========================
class Compra(models.Model):                              # Modelo que registra una compra realizada
    METODOS_PAGO = [                                     # Métodos de pago válidos
        ('Tarjeta', 'Tarjeta'),
    ]

    ESTATUS_COMPRA = [                                   # Estado de la compra
        ('Completada', 'Completada'),
    ]

    usuario = models.ForeignKey(                         # Relación con el usuario que realizó la compra
        Usuario,
        on_delete=models.CASCADE,
        related_name='compras'
    )
    detalles_productos = models.JSONField(default=list)  # Lista de productos incluidos en la compra
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total pagado
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)  # Método utilizado
    estatus = models.CharField(                          # Estatus de la compra
        max_length=20,
        choices=ESTATUS_COMPRA,
        default='Completada'
    )
    fecha_compra = models.DateTimeField(auto_now_add=True)  # Fecha y hora automática al crearse

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"  # Representación legible
