from django.shortcuts import render,redirect
from django.db import Error,transaction
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
import urllib
import json
# Librerias para envio de correo
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading # Hilos envió de correo
from smtplib import SMTPException
from appGestionInventario.models import *
import random
import string
import os


# Create your views here.

def vistaLogin(request):
    return render(request,"frmIniciarSesion.html")

def login(request):
    # Validar el recaptcha 
    ''' Begin reCAPTCHA validation'''
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print(result)
    ''' End reCAPTCHA validation'''
    
    if result['success']:
        print("Prueba")
        username = request.POST["txtUsername"]
        password = request.POST["txtPassword"]
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            print(username)
            # Registrar la variable de sesión
            auth.login(request,user)
            if user.groups.filter(name='Administrador').exists():
                print("Ingresando administrador")
                return redirect ('/inicioAdministrador')
            elif user.groups.filter(name='Asistente').exists():
                print("Ingresando asistente")
                return redirect('/inicioAsistente')
            else:
                print("Ingresando instructor")
                return redirect('/inicioInstructor')
        else:
            mensaje = "Usuario o Contraseña Incorrectas"
            return render(request,"frmIniciarSesion.html",{"mensaje":mensaje})
    else: 
        mensaje = "Debe validar primero el recaptcha"
        return render(request,"frmIniciarSesion.html",{"mensaje":mensaje})

def enviarCorreo(asunto=None,mensaje=None,destinatario=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatario':destinatario,
        'mensaje':mensaje,
        'asunto':asunto,
        'remitente':remitente
    })
    try:
        correo = EmailMultiAlternatives(asunto,mensaje,remitente,[destinatario])
        correo.attach_alternative(contenido, 'text/html')
        correo.send(fail_silently=True)
    except SMTPException as error:
        print(error)
     
def inicioInstructor(request):
    if request.user.is_authenticated:
        return render(request,"instructor/inicio.html")
    else:
        retorno = {"mensaje":"Debe ingresar con sus crendeciales correctas"}
        return render(request,"frmIniciarSesion.html",retorno)
    
def inicioAsistente(request):
    if request.user.is_authenticated:
        return render(request,"asistente/inicio.html")
    else:
        retorno = {"mensaje":"Debe ingresar con sus crendeciales correctas"}
        return render(request,"frmIniciarSesion.html",retorno)
    
def inicioAdministrador(request):
    if request.user.is_authenticated:
        return render(request,"administrador/inicio.html")
    else:
        retorno = {"mensaje":"Debe ingresar con sus crendeciales correctas"}
        return render(request,"frmIniciarSesion.html",retorno)

def generarPassword():
    longitud = 10
    caracteres = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password = ''
    for i in range(longitud):
        password += ''.join(random.choice(caracteres))
    return password

def registrarUsuario(request):
    try:
        nombre = request.POST["txtNombre"]
        apellido = request.POST["txtApellido"]
        correo = request.POST["txtCorreo"]
        tipo = request.POST["cbTipo"]
        foto = request.FILES.get("Fimagen")
        idRol = int(request.POST["cbRol"])
        with transaction.atomic():
            # Crear un objeto de tipo User
            user = User(username=correo,first_name=nombre,
                        last_name=apellido,email=correo,
                        userTipo=tipo,userFoto=foto)
            user.save()
            # Obtener el Rol de acuerdo a su id del rol
            rol = Group.objects.get(pk=idRol)
            # Agregar el usuario a ese Rol
            user.groups.add(rol)
            # Si el rol es Administrador se habilita para que tenga acceso
            # al sitio web del administrador
            if (rol.name == "Administrador"):user.is_staff = True
            # Guardamos el usuario con lo que tenemos 
            user.save()
            # Llamamos a la funcion generarPassword
            passwordGenerado = generarPassword()
            print (f"password {passwordGenerado}")
            # Con el usuario creado llamamos a la funcion set_password que 
            # encripta el password y lo agrega al campo password del user
            user.set_password(passwordGenerado)
            # Se actualiza el user 
            user.save()
            mensaje = "Usuario agregado correctamente"
            retorno ={"mensaje":mensaje}
            # Enviar correo cliente
            asunto = 'Registro en nuestro Sistema CIES-NEIVA'
            mensaje = f'Cordial Saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos \
                informarle que usted ha sido registrado en nuestro Sistema de Gestión de Inventario \
                del Centro de la Industria, la Empresa y los Servicios CIES de la ciudad de Neiva. \
                Sus datos para ingresar a nuestro sistema son los siguientes:<br> \
                <br><b>Username: </b> {user.username} \
                <br><b>Password: </b> {passwordGenerado} \
                <br><br>Lo invitamos a ingresar a nuestro sistema mediante el siguiente link: \
                https://gestioninventario.sena.edu.co'
            thread = threading.Thread(target=enviarCorreo,
                                    args=(asunto,mensaje,user.email))
            thread.start()
            return redirect("/vistaGestionUsuarios/",retorno)
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
    retorno = {"mensaje":mensaje, "user":user}
    return render(request, "administrador/frmRegistrarUsuario.html",retorno)

def vistaRegistrarUsuarios(request):
    roles = Group.objects.all()
    tipos = tipoUsuario
    retorno = { "tipos":tipos,"roles":roles, "user":None}
    return render(request, "administrador/frmRegistrarUsuario.html",retorno)

def vistaGestionUsuarios(request):
    try:
        usuarios = User.objects.all()
        mensaje=""
    except Error as error:
        mensaje =f"problemas al listar los usuarios {error}"

    retorno = {"mensaje": mensaje, "listaUsuarios":usuarios }
    return render(request,"administrador/gestionarUsuarios.html", retorno)

def eliminarUsuario(request,id):
    try:
        usuarios = User.objects.get(id=id)
        if usuarios.userFoto:
            imagen = usuarios.userFoto.path
            if os.path.exists(imagen):
                os.remove(imagen)
        usuarios.delete()
        mensaje = "Usuario eliminado"
    except Error as error:
        mensaje = f"Problemas al eliminar el producto {error}"
    retorno = {"mensaje":mensaje}
    return redirect("/vistaGestionUsuarios/",retorno)

def consultarUsuario(request,id):
    try:
        usuario = User.objects.get(id=id)
        roles = Group.objects.all()
        tipos = tipoUsuario
        mensaje = ""
        
    except Error as error:
        mensaje = f"Problemas al consultar {error}"
        
    retorno = {"tipos":tipos,"roles":roles,"mensaje":mensaje,"usuario":usuario}
    return render (request,"administrador/frmEditarUsuario.html",retorno)

def actualizarUsuario(request):
    idUsuario = request.POST["idUsuario"]
    nombre = request.POST["txtNombre"]
    apellido = request.POST["txtApellido"]
    correo = request.POST["txtCorreo"]
    tipo = request.POST["cbTipo"]
    foto = request.FILES.get("Fimagen")
    try:
        # Obtener el tipo de acuerdo al ingresado
        tipoUsuario = tipo
        # Actualizar el usuario, primero se consulta
        usuario = User.objects.get(id=idUsuario)
        usuario.username = correo
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.userTipo = tipo
        # Si el campo de foto tiene datos actualiza foto
        if foto:
            usuario.userFoto = foto
        else:
            usuario.userFoto = usuario.userFoto
        usuario.save()
        mensaje = "Usuario actualizado correctamente"
        return redirect("/vistaGestionUsuarios/")
    except Error as error:
        mensaje = f"Problemas al realizar el proceso de actualizar el usuario {error}"
    tipo = tipoUsuario
    retorno = {"mensaje":mensaje,"tipos":tipo,"usuario":usuario}
    return render (request,"frmEditarUsuario.html",retorno)

def vistaGestionarDevolutivos(request):
    if request.user.is_authenticated:
        elementosDevolutivos = Devolutivo.objects.all()
        retorno = {"listaElementosDevolutivos": elementosDevolutivos}
        print(elementosDevolutivos)
        return render(request,"administrador/vistaGestionarElementos.html",retorno)
    else:
        mensaje = "Debe iniciar sesión primero"
        return render(request,"frmIniciarSesion.html",mensaje)
    
def vistaRegistrarDevolutivo(request):
    retorno = {"tipoElementos":tipoElemento,"estados":estadosElementos}
    print(retorno)
    return render(request,"administrador/frmRegistrarDevolutivo.html",retorno)

def registrarDevolutivo(request):
    estado = False
    try:
        placaSena = request.POST["txtPlacaSena"]
        fechaInventarioSena = request.POST["txtFechaSena"]
        tipoElemento  = request.POST["cbTipoElemento"]
        serial = request.POST.get("txtSerial",False)
        marca = request.POST.get("txtMarca",False)
        valorUnitario = int(request.POST["txtValorUnitario"])
        estado = request.POST["cbEstado"]
        nombre = request.POST["txtNombre"]
        descripcion = request.POST["txtDescripcion"]
        deposito = request.POST["cbDeposito"]
        estante = request.POST.get("txtEstante",False)
        entrepano = request.POST.get("txtEntrepano",False)
        locker = request.POST.get("txtLocker",False)
        archivo = request.FILES.get("Fimagen",False)
        with transaction.atomic():
            # Obtener cuantos elementos se han registrado
            cantidad = Elemento.objects.all().count()
            # Crear un codigo a partir de la cantidad ajustando el inicio
            codigoElemento = tipoElemento.upper() + str(cantidad+1).rjust(6,'0')
            # Crear el elemento
            elemento = Elemento(eleCodigo=codigoElemento,eleNombre=nombre,eleTipo=tipoElemento,eleEstado=estado)
            # Guardar el elemento en la base de datos
            elemento.save()
            # Crear objeto ubicacion fisica del elemento
            ubicacion = UbicacionFisica(ubiDeposito=deposito,ubiEstante=estante,ubiEntrepano=entrepano,ubiLocker=locker,ubiElemento=elemento)
            # Registrar en la base de datos la ubicacion fisica del elemento
            ubicacion.save()
            # Crear el devolutivo
            elementoDevolutivo = Devolutivo(devPlacaSena=placaSena,devSerial=serial,
                                            devDescripcion=descripcion,devMarca=marca,
                                            devFechaIngresoSENA=fechaInventarioSena,
                                            devValor=valorUnitario,devFoto=archivo,
                                            devElemento=elemento)
            elementoDevolutivo.save()
            estado = True
            mensaje = f'Elemento Devolutivo registrado satisfactoriamente con el codigo{codigoElemento}'
    except Error as error:
        transaction.rollback()
        mensaje ="Error"
    retorno = {"mensaje":mensaje,"devolutivo":elementoDevolutivo,"estado":estado}
    return render (request,"administrador/frmRegistrarDevolutivo.html",retorno) 