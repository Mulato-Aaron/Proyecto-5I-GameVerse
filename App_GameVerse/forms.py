from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Usuario, Producto, Proveedor
import re


# =====================================================
# VALIDACIÓN PERSONALIZADA PARA CONTRASEÑAS
# =====================================================

def validar_password(value):
    # Verifica que la contraseña solo contenga letras y números.
    if not re.match(r'^[A-Za-z0-9]+$', value):
        raise ValidationError("La contraseña solo puede contener letras y números (sin caracteres especiales).")

    # Verifica la longitud mínima requerida (8 caracteres).
    if len(value) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

    # Verifica que tenga al menos una letra y un número para mayor seguridad.
    if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
        raise ValidationError("La contraseña debe contener al menos una letra y un número.")


# -------------------------
# FORMULARIO PROVEEDOR
# -------------------------
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'tipo', 'pais', 'sitio_web', 'descripcion', 'estatus']


# -------------------------
# FORMULARIO PRODUCTO
# -------------------------
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'tipo', 'genero', 'descripcion', 'precio',
            'fecha_lanzamiento', 'proveedor', 'calificacion_promedio',
            'disponible', 'imagen'
        ]


# -------------------------
# FORMULARIO USUARIO
# -------------------------
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'fecha_nacimiento', 'pais', 'estatus', 'is_superuser']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})
        }


# =====================================================
# FORMULARIO DE REGISTRO (CON VALIDACIÓN DE CONTRASEÑA)
# =====================================================
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Nuevo campo adicional
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})  # Selector de fecha moderno
    )
    pais = forms.CharField(max_length=50, required=False)  # Campo agregado por el usuario

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'fecha_nacimiento', 'pais', 'password1', 'password2')

    # 🚀 VALIDACIÓN NUEVA: aplica reglas personalizadas a password1
    def clean_password1(self):
        password = self.cleaned_data.get("password1")  # Recupera la contraseña ingresada
        if password:
            validar_password(password)  # Llama al validador personalizado
        return password  # Devuelve la contraseña validada


# -------------------------
# FORMULARIO DE LOGIN
# -------------------------
class LoginForm(AuthenticationForm):
    pass


# -------------------------
# FORMULARIO DE CUENTA
# -------------------------
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'pais', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
        }


# =====================================================
# FORMULARIO DE MÉTODO DE PAGO
# =====================================================
class MetodoPagoForm(forms.Form):
    METODOS = [
        ('Tarjeta', 'Tarjeta'),
        ('Efectivo', 'Efectivo'),
        ('Credito', 'Crédito de la cuenta'),  # ← Método agregado por ti
    ]

    metodo_pago = forms.ChoiceField(
        choices=METODOS,  # Lista de métodos disponibles
        widget=forms.RadioSelect,  # Campos tipo "radio button"
        label="Selecciona tu método de pago"
    )

    telefono = forms.CharField(
        max_length=15,
        label="Teléfono",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu teléfono'})
    )

    direccion = forms.CharField(
        max_length=200,
        label="Dirección",
        required=True,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ingresa tu dirección'})
    )


# =====================================================
# FORMULARIO DE PAGO CON TARJETA
# =====================================================
class PagoTarjetaForm(forms.Form):
    nombre_tarjeta = forms.CharField(max_length=100, label="Nombre en la tarjeta")
    numero_tarjeta = forms.CharField(max_length=16, min_length=16, label="Número de tarjeta")
    mes_expiracion = forms.IntegerField(min_value=1, max_value=12, label="Mes de expiración")
    anio_expiracion = forms.IntegerField(min_value=2024, max_value=2100, label="Año de expiración")
    cvv = forms.CharField(max_length=4, min_length=3, label="CVV")

    def clean(self):
        cleaned_data = super().clean()  # Recupera todos los campos ya validados

        mes = cleaned_data.get("mes_expiracion")
        anio = cleaned_data.get("anio_expiracion")

        # Se obtiene la fecha actual para comparar
        hoy = timezone.now()

        # Validación nueva: la tarjeta es válida si expira este mes o después
        if mes and anio:
            if anio < hoy.year or (anio == hoy.year and mes < hoy.month):
                raise ValidationError("❌ La tarjeta está vencida.")

        return cleaned_data


# =====================================================
# FORMULARIO PARA AGREGAR CRÉDITO
# =====================================================
class AgregarCreditoForm(forms.Form):
    credito = forms.DecimalField(max_digits=10, decimal_places=2, label="Monto a agregar")
    nombre_tarjeta = forms.CharField(max_length=100)
    numero_tarjeta = forms.CharField(max_length=20)
    mes_expiracion = forms.IntegerField(min_value=1, max_value=12)
    anio_expiracion = forms.IntegerField(min_value=2024, max_value=2100)
    cvv = forms.CharField(max_length=4)

    def clean(self):
        cleaned_data = super().clean()

        mes = cleaned_data.get("mes_expiracion")
        anio = cleaned_data.get("anio_expiracion")

        # Obtención de la fecha actual para comparar
        hoy = timezone.now()

        # Validación nueva igual que en PagoTarjetaForm
        if mes and anio:
            if anio < hoy.year or (anio == hoy.year and mes < hoy.month):
                raise ValidationError("❌ La tarjeta está vencida.")

        return cleaned_data

class DevolucionForm(forms.Form):
    OPCIONES = [
        ("credito", "Reembolso a crédito"),
        ("tarjeta", "Reembolso a tarjeta / depósito bancario"),
    ]

    metodo = forms.ChoiceField(choices=OPCIONES, widget=forms.RadioSelect)

    # Campos solo requeridos si elige tarjeta / depósito
    titular = forms.CharField(required=False)
    numero = forms.CharField(required=False)
    banco = forms.CharField(required=False)

    def clean(self):
        data = super().clean()

        if data["metodo"] == "tarjeta":
            if not data["titular"] or not data["numero"] or not data["banco"]:
                raise forms.ValidationError(
                    "Debes llenar los datos bancarios para el reembolso por tarjeta/deposito."
                )

        return data
