from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password #Compara contraseña con Hash
from .models import Usuario
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required




#FUNCION PARA VERIFICAR SI EL USUARIO ES ADMIN
# Esta funcion se utiliza para verificar si el usuario logueado es un administrador.
def usuario_es_admin(request):
    return request.session.get('usuario_rol') == 'admin'


#LISTAR USUARIOS
# Esta vista lista todos los usuarios registrados en la base de datos.
def listar_usuarios(request):
    if not usuario_es_admin(request):
        messages.error(request, 'No tenes permiso para ver esta seccion.')
        return redirect('inicio')

    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})


#CREAR USUARIO
# Esta vista permite a los administradores crear nuevos usuarios.
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
# Esta vista permite a los administradores editar la información de un usuario existente.
def editar_usuario(request, id):
    if not usuario_es_admin(request):
        messages.error(request, 'No tenes permiso para acceder.')
        return redirect('inicio')

    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('listar_usuarios')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        confirmar = request.POST.get('confirmar')

        # Validaciones
        if email != usuario.email and Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya esta registrado a otro usuario.')
            return render(request, 'editar_usuario.html', {'usuario': usuario})

        if password:
            if password != confirmar:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'editar_usuario.html', {'usuario': usuario})
            else:
                usuario.password = make_password(password)

        usuario.nombre = nombre
        usuario.email = email
        usuario.rol = rol
        usuario.save()

        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('listar_usuarios')

    return render(request, 'editar_usuario.html', {'usuario': usuario})


#ELIMINAR USUARIO
# Esta vista permite a los administradores eliminar un usuario existente.
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
# Esta vista guarda el rol del usuario en la sesion de manera protegida.
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
# Esta vista maneja el cierre de sesion de los usuarios.
def logout_usuario(request):
    request.session.flush()  
    return redirect('login_usuario')


#LOGIN DE USUARIO
# Esta vista maneja el inicio de sesion de los usuarios.
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
# Esta vista maneja el registro de nuevos usuarios.
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

        #Hashear contraseña antes de guardar
        hashed_password = make_password(password)

        usuario = Usuario(nombre=nombre, email=email, password=hashed_password)
        usuario.save()

        messages.success(request, 'Usuario creado correctamente. Ahora podes iniciar sesion.')
        return redirect('login_usuario')

    return render(request, 'registrar.html')


#POKEDEX
# Esta vista renderiza la página principal de la Pokedex, asegurando que el usuario esté logueado.
def pokedex(request):
    if 'usuario_id' not in request.session:
        return redirect('login_usuario') 
    return render(request, 'pokedex.html')