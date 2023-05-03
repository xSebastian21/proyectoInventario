from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

estadosMantenimiento =[
    ('Sastisfactorio','Satisfactorio'),
    ('Requiere Ajuste','Requiere Ajuste'),
    ('Requiere Reparacion','Requiere Reparacion'),
    ('Requiere Reemplazo','Requiere Reemplazo'),
    ('Defecto Corregido','Defecto Corregido'),
]

tipoProveedor = [
    ('PJ','Persona Juridica'),
    ('PN','Persona Natural')
]

tipoUsuario = [
    ('Instructor','Instructor'),
    ('Aprendiz','Aprendiz'),
    ('Administrativo','Administrativo')
]

class Ficha(models.Model):
    ficCodigo = models.IntegerField(unique=True, db_comments="Codigo de la Ficha")
    ficNombre = models.CharField(max_length=100, db_comments="Nombre de la Ficha")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora Ultima Actualizacion")
    
    def __str__(self)->str:
        return f"{self.ficCodigo} - {self.ficNombre}"
    
class UnidadMedida(models.Model):
    uniNombre = models.CharField(max_length=45,unique=True,db_comments="Nombre de la unidad de medida")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora Ultima Actualizacion")
    
    def __str__(self) -> str:
        return f"{self.uniNombre}"
    
class EstadoMantenimiento(models.Model):
    estNombre = models.CharField(max_length=45,unique=True,choices=estadosMantenimiento)
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora Ultima Actualizacion")
    
    def __str__(self) -> str:
        return f"{self.estNombre}"
    
class Proveedor(models.Model):
    proTipo = models.CharField(max_length=2,choices=tipoProveedor, db_comments="Tipo de proveedor")
    proIdentificacion = models.CharField(max_length=15,unique=True,
                                        db_comments="Identificacion del proveedor, puede ser Cedula o Nit")
    proNombre = models.CharField(max_length=60,db_comments="Nombre del proveedor")
    proRepresentanteLegal = models.CharField(max_length=60,null=True,
                                        db_comments="Nombre del representante legal si es persona Júridica")
    proTelefono = models.IntegerField(max_length=15,null=True, 
                                        db_comments="Numero Telefono del proveedor")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora Ultima Actualizacion")
    
    def __str__(self) -> str:
        return f"{self.proNombre}"
    
class User(AbstractUser):
    userFoto = models.FileField(upload_to=f"fotos/",null=True,blank=True,db_comments="Foto del Usuario")
    userTipo = models.CharField(max_length=15,choices=tipoUsuario,
                                db_comments = "Nombre Tipo de Usuario")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True ,db_comments="Fecha y Hora Ultima Actualizacion")
    
    def __str__(self) -> str:
        return f"{self.username}"