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
    if not re.match(r'^[A-Za-z0-9]+$', value):
        raise ValidationError("La contraseña solo puede contener letras y números (sin caracteres especiales).")

    if len(value) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

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
        widgets = {
            'fecha_lanzamiento': forms.DateInput(attrs={'type': 'date'})
        }


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
# FORMULARIO DE REGISTRO
# =====================================================
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    pais = forms.CharField(max_length=50, required=False)

    seguridad = None

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'fecha_nacimiento', 'pais', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password:
            validar_password(password)
            self.seguridad = evaluar_seguridad(password)
        return password


def evaluar_seguridad(password):
    puntaje = 0

    if len(password) >= 8:
        puntaje += 1
    if re.search(r"[A-Z]", password):
        puntaje += 1
    if re.search(r"[a-z]", password):
        puntaje += 1
    if re.search(r"\d", password):
        puntaje += 1

    if puntaje <= 1:
        return "muy débil"
    elif puntaje == 2:
        return "débil"
    elif puntaje == 3:
        return "moderada"
    else:
        return "fuerte"


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
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'  # ← FORMATO CORRECTO PARA HTML5
            ),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace que Django precargue la fecha con el formato correcto
        if self.instance and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].initial = (
                self.instance.fecha_nacimiento.strftime('%Y-%m-%d')
            )



# =====================================================
# FORMULARIO DE MÉTODO DE PAGO
# =====================================================
class MetodoPagoForm(forms.Form):
    METODOS = [
        ('Tarjeta', 'Tarjeta'),
        ('Credito', 'Crédito de la cuenta'),
    ]

    metodo_pago = forms.ChoiceField(
        choices=METODOS,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Selecciona tu método de pago"
    )

    telefono = forms.CharField(
        max_length=15,
        label="Teléfono",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu teléfono'
        })
    )

    direccion = forms.CharField(
        max_length=200,
        label="Dirección",
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Ingresa tu dirección'
        })
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
        cleaned_data = super().clean()
        mes = cleaned_data.get("mes_expiracion")
        anio = cleaned_data.get("anio_expiracion")
        hoy = timezone.now()

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
    mes_expiracion = forms.IntegerField(min_value=1, max_value=12, label="Mes de expiración")
    anio_expiracion = forms.IntegerField(min_value=2024, max_value=2100, label="Año de expiración")
    cvv = forms.CharField(max_length=4)

    def clean(self):
        cleaned_data = super().clean()
        mes = cleaned_data.get("mes_expiracion")
        anio = cleaned_data.get("anio_expiracion")
        hoy = timezone.now()

        if mes and anio:
            if anio < hoy.year or (anio == hoy.year and mes < hoy.month):
                raise ValidationError("❌ La tarjeta está vencida.")

        return cleaned_data


# =====================================================
# FORMULARIO DE DEVOLUCIÓN
# =====================================================
class DevolucionForm(forms.Form):
    OPCIONES = [
        ("credito", "Reembolso a crédito"),
        ("tarjeta", "Reembolso a tarjeta / depósito bancario"),
    ]

    metodo = forms.ChoiceField(choices=OPCIONES, widget=forms.RadioSelect)
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
