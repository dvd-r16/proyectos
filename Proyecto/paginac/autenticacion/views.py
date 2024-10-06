# from msilib.schema import ListView
from django.views.generic import ListView, View
from unicodedata import name
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from autenticacion.utils import render_to_pdf
from .forms import CustomUserCreationForm  
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import itertools
from pedidos.models import Pedido
from pedidos.models import LineaPedido
from inventario.models import articulos
from usuarios.models import usuarios
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from axes.utils import reset
from django.contrib.auth.decorators import user_passes_test
from usuarios.models import Profesor  # Asegúrate de tener este modelo correctamente importado
from inventario.models import articulos
from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()

# Vista de registro de usuarios
class VRegistro(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registro/registro.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            # Guardamos el usuario en el modelo User
            usuario = form.save()

            # Ahora extraemos los campos adicionales para guardarlos en el modelo usuarios
            
            birth_date = request.POST.get('birth_date')  # Estos campos no están en User
            cui = request.POST.get('cui')
            phone = request.POST.get('phone')
            profile_image = request.FILES.get('profile_image')

            # Creamos el registro en la tabla usuarios
            nuevo_usuario = usuarios(user=usuario, cui=cui, birth_date=birth_date, phone=phone, profile_image=profile_image)
            nuevo_usuario.save()

            # Autenticamos y logueamos al usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(request=request, username=username, password=password)
            login(request, usuario)

            return redirect('Home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "registro/registro.html", {"form": form})

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('Home')

# Vista para iniciar sesión
def iniciar_sesion(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(request=request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                reset(username=username)
                return redirect('Home')
            else:
                messages.error(request, "Usuario no válido")
        else:
            messages.error(request, "Información no válida")

    form = AuthenticationForm()
    return render(request, "login/login.html", {"form": form})

# Vista de perfil de usuario
def perfil(request):
    user = request.user
    usuario_detalles = user.profile if hasattr(user, 'profile') else None

    if hasattr(user, 'profesor'):
        # Si el usuario es un profesor, obtener los cursos que imparte
        profesor = Profesor.objects.get(user=user)
        cursos_asignados = articulos.objects.filter(catedratico=profesor)
        context = {
            "user": user,
            "profesor": profesor, #Información del profesor
            "cursos_a_impartir": cursos_asignados  # Enviamos los cursos que imparte el profesor
        }
        return render(request, "perfil/perfil_profesor.html", context)

    else:
        articulos_comprados = LineaPedido.objects.all()
        pedidos_comprados = Pedido.objects.all()
        listado_todos_productos = articulos.objects.all()

    context= {
        "user": user,
        "usuario_detalles": usuario_detalles,  # Enviamos la información adicional del usuario
        "articulos_comprados": articulos_comprados,
        "listado_todos_productos": listado_todos_productos,
        "pedidos_comprados": pedidos_comprados
    }
    
    return render(request, "perfil/perfil.html", context)

# Vista para generar PDF del perfil
class perfil_pdf(View):
    def get(self, request, *arg, **kwargs):
        user_id = request.user.id
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

        user = {
            'id': user_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

        articulos_comprados = LineaPedido.objects.all()
        listado_todos_productos = articulos.objects.all()
        pedidos_comprados = Pedido.objects.all()

        articulos_comprados2 = []
        listado_todos_productos2 = []
        for articulos_comprados in articulos_comprados:
            if articulos_comprados.user_id == user_id:
                articulos_comprados2.append(articulos_comprados)
                articulo = articulos.objects.get(pk=articulos_comprados.producto_id)
                listado_todos_productos2.append(articulo)
        
        data = {
            'articulos_comprados': articulos_comprados2,
            'listado_todos_productos': listado_todos_productos,
            'pedidos_comprados': pedidos_comprados,
            'user': user
        }
        pdf = render_to_pdf('perfil/perfil_pdf.html', data)

        return HttpResponse(pdf, content_type='application/pdf')

# Vista de bloqueo por intentos fallidos de inicio de sesión
def lockout(request, credentials, *args, **kwargs):
    for i in User.objects.all():
        if i.username == credentials["username"]:
            correo_usuario = i.email
    try:
        enviar_mail(
            nombreusuario=credentials["username"],
            emailusuario=correo_usuario
        )
    except:
        print("No se ha podido enviar el correo")

    return render(request, "lockout/lockout.html")

# Función para enviar correo de restablecimiento de contraseña
def enviar_mail(**kwargs):

    asunto = "Restablecimiento Contraseña en Kaori Shop"
    mensaje = render_to_string("emails/reset_pass.html", {
        "nombreusuario": kwargs.get("nombreusuario")
    })

    mensaje_texto = strip_tags(mensaje)
    from_email = "fiusac.recuperacion@gmail.com"
    to = kwargs.get("emailusuario")

    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)

def es_profesor(user):
    return hasattr(user, 'profesor')  # Asume que el modelo Profesor está relacionado con el usuario

@user_passes_test(es_profesor)
def profesor_panel(request):
    return render(request, 'autenticacion/profesor_panel.html')