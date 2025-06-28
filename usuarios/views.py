from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password #Compara contraseña con Hash
from .models import Usuario
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def audio_player(request):
    return render(request, 'audio_player.html')

#FUNCION PARA VERIFICAR SI EL USUARIO ES ADMIN
def usuario_es_admin(request):
    return request.session.get('usuario_rol') == 'admin'


#LISTAR USUARIOS
def listar_usuarios(request):
    rol = request.session.get('usuario_rol')
    if rol not in ['admin', 'editor']:
        messages.error(request, 'No tenés permiso para ver esta sección.')
        return redirect('inicio')

    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {
        'usuarios': usuarios,
        'rol': rol  #pasamos el rol al template para ocultar botones
    })

#CREAR USUARIO
def crear_usuario(request):
    if not usuario_es_admin(request):
        messages.error(request, 'No tenés permiso para acceder.')
        return redirect('inicio')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')
        rol = request.POST.get('rol')

        if password != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'crear_usuario.html')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya esta registrado.')
            return render(request, 'crear_usuario.html')

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=make_password(password),
            rol=rol
        )
        nuevo_usuario.save()

        messages.success(request, 'Usuario creado correctamente.')
        return redirect('listar_usuarios')

    return render(request, 'crear_usuario.html')


#EDITAR USUARIO
def editar_usuario(request, id):
    if 'usuario_id' not in request.session:
        messages.error(request, 'Tenés que iniciar sesión.')
        return redirect('login_usuario')

    usuario_logueado = Usuario.objects.get(id=request.session['usuario_id'])
    rol_logueado = request.session.get('usuario_rol')

    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('listar_usuarios')

    #editor NO puede editar un usuario admin
    if rol_logueado == 'editor' and usuario.rol == 'admin':
        messages.error(request, 'No tenés permiso para editar a un administrador.')
        return redirect('listar_usuarios')

    #viewer ni otro sin rol editan
    if rol_logueado not in ['admin', 'editor']:
        messages.error(request, 'No tenés permiso para acceder.')
        return redirect('inicio')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        nuevo_rol = request.POST.get('rol')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')

        if email != usuario.email and Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado a otro usuario.')
            return render(request, 'editar_usuario.html', {'usuario': usuario})

        if password:
            if password != confirmar:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'editar_usuario.html', {'usuario': usuario})
            else:
                usuario.password = make_password(password)

        usuario.nombre = nombre
        usuario.email = email

        #solo el admin puede cambiar el rol
        if rol_logueado == 'admin':
            usuario.rol = nuevo_rol

        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('listar_usuarios')

    return render(request, 'editar_usuario.html', {'usuario': usuario})




#ELIMINAR USUARIO
def eliminar_usuario(request, id):
    if not usuario_es_admin(request):
        messages.error(request, 'No tenés permiso para acceder.')
        return redirect('inicio')

    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('listar_usuarios')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('listar_usuarios')

    #Confirmar antes de eliminar
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})


#OBJETO DE SESION
def inicio(request):
    if 'usuario_id' not in request.session:
        return redirect('login_usuario')  

    rol = request.session.get('usuario_rol')
    nombre = Usuario.objects.get(id=request.session['usuario_id']).nombre

    return render(request, 'inicio.html', {
        'rol': rol,
        'nombre': nombre
    })


#LOGOUT DE USUARIO
def logout_usuario(request):
    request.session.flush()  
    return redirect('login_usuario')


#LOGIN DE USUARIO
def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'Email o contraseña incorrectos.')
            return render(request, 'login.html')

        if check_password(password, usuario.password):
            #id del usuario en sesion para marcar que esta logueado
            request.session['usuario_id'] = usuario.id
            request.session['usuario_rol'] = usuario.rol
            return redirect('inicio')  
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
            return render(request, 'login.html')

    return render(request, 'login.html')


#REGISTRO DE USUARIO
def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')

        if password != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registrar.html')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Ese email ya esta registrado.')
            return render(request, 'registrar.html')

        #Hashear contrasena antes de guardar
        hashed_password = make_password(password)

        usuario = Usuario(nombre=nombre, email=email, password=hashed_password)
        usuario.save()

        messages.success(request, 'Usuario creado correctamente. Ahora podes iniciar sesion.')
        return redirect('login_usuario')

    return render(request, 'registrar.html')


#POKEDEX
def pokedex(request):
    if 'usuario_id' not in request.session:
        return redirect('login_usuario') 
    return render(request, 'pokedex.html')