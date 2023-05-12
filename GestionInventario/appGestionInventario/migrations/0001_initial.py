# Generated by Django 4.2.1 on 2023-05-05 11:51

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userFoto', models.FileField(blank=True, db_comment='Foto del Usuario', null=True, upload_to='fotos/')),
                ('userTipo', models.CharField(choices=[('Aprendiz', 'Aprendiz'), ('Instructor', 'Instructor'), ('Administrativo', 'Administrativo')], db_comment='Nombre Tipo de usuario', max_length=15)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detCantidadRequerida', models.IntegerField(db_comment='Cantidad requerida del elemento')),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Elemento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eleCodigo', models.CharField(db_comment='Código único asignado al elemento', max_length=15, unique=True)),
                ('eleNombre', models.CharField(db_comment='Nombre del Elemento', max_length=50)),
                ('eleTipo', models.CharField(choices=[('HER', 'Herramientas'), ('MAQ', 'Maquinaria'), ('EQU', 'Equipos'), ('MAT', 'Materiales')], db_comment='Tipo de Elemento', max_length=3)),
                ('eleEstado', models.CharField(choices=[('Bueno', 'Bueno'), ('Bueno', 'Regular'), ('Bueno', 'Malo')], db_comment='Estado del elemento devolutivo', max_length=10)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoMantenimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estNombre', models.CharField(choices=[('Satisfactorio', 'Satisfactorio'), ('Requiere Ajuste', 'Requiere Ajuste'), ('Requiere Reparación', 'Requiere Reparación'), ('Requiere Remplazo', 'Requiere Remplazo'), ('Defecto Corregido', 'Defecto Corregido')], db_comment='Nombre del estado del mantenimiento', max_length=50, unique=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ficCodigo', models.IntegerField(db_comment='Código de la Ficha', unique=True)),
                ('ficNombre', models.CharField(db_comment='Nombre del programa de la Ficha', max_length=100)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proTipo', models.CharField(choices=[('Persona Júridica', 'Persona Júridica'), ('Persona Natural', 'Persona Natural')], db_comment='Tipo de proveedor', max_length=20)),
                ('proIdentificacion', models.CharField(db_comment='Identificación del proveedor, puede ser cédula o Nit', max_length=15, unique=True)),
                ('proNombre', models.CharField(db_comment='Nombre del proveedor', max_length=60)),
                ('proRepresentanteLegal', models.CharField(db_comment='Nombre representante legal si es persona Júridica', max_length=60, null=True)),
                ('proTelefono', models.CharField(db_comment='Número telefono del proveedor', max_length=15, null=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniNombre', models.CharField(db_comment='Nombre de la Unidad de Médida', max_length=45, unique=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='UbicacionFisica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubiDeposito', models.SmallIntegerField(db_comment='Número de bodega: 1,2,3,4..')),
                ('ubiEstante', models.SmallIntegerField(db_comment='Número de bodega: 1,2,3,4..', null=True)),
                ('ubiEntrepano', models.SmallIntegerField(db_comment='Número de Entrepaño: 1,2,3,4..', null=True)),
                ('ubiLocker', models.SmallIntegerField(db_comment='Número de locker: 1,2,3,4..', null=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('ubiElemento', models.ForeignKey(db_comment='Hace referencia al elemento', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.elemento')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudElemento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solProyecto', models.TextField(db_comment='Nombre proyecto que el instructor está desarrollando con la ficha')),
                ('solFechaHoraRequerida', models.DateTimeField(db_comment='Fecha y hora que requiere los elementos', null=True)),
                ('solEstado', models.CharField(choices=[('Solicitada', 'Solicitada'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada'), ('Atendida', 'Atendida'), ('Cancelada', 'Cancelada')], db_comment='Estado de la solicitud', max_length=10)),
                ('solObservaciones', models.TextField(db_comment='Alguna observación que el instructor quiera agregar en la solicitud', null=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('solFicha', models.ForeignKey(db_comment='Ficha en la que el instructor utilizará los elementos', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.ficha')),
                ('solUsuario', models.ForeignKey(db_comment='Usuario instructor que hace la solicitud', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalidaDetalleSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salCantidadEntregada', models.IntegerField(db_comment='Cantidad entregada')),
                ('salObservaciones', models.TextField(db_comment='Observaciobes que el asistente quiera agregar', null=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('salDetalleSolicitud', models.ForeignKey(db_comment='Hace referencia al detalle de la solicitud', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.detallesolicitud')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matReferencia', models.TextField(db_comment='Referencia o descripción del material', null=True)),
                ('matMarca', models.CharField(db_comment='Marca del material si tiene', max_length=50, null=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('matElemento', models.ForeignKey(db_comment='Hace referencia al Elemento FK', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.elemento')),
                ('matUnidadMedida', models.ForeignKey(db_comment='Hace referencia a la Unidad de Medida FK', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.unidadmedida')),
            ],
        ),
        migrations.CreateModel(
            name='Mantenimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manObservaciones', models.TextField(db_comment='Observaciones que se quieran agregar                                 al mantenimiento', null=True)),
                ('manFechaHoraMantenimiento', models.DateTimeField(db_comment='Hace referencia a la fecha y hora que                                 se realizó el mantenimiento')),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('manElemento', models.ForeignKey(db_comment='Hace referencia al elemento que se le realizó el mantenimiento', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.elemento')),
                ('manEstado', models.ForeignKey(db_comment='Hace referencia al estado del mantenimiento', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.estadomantenimiento')),
                ('manUsuario', models.ForeignKey(db_comment='Hace referencia al usuario que realizó el mantenimiento', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EntradaMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entNumeroFactura', models.CharField(db_comment='Número de la factura', max_length=15)),
                ('entFechaHora', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora que entregan los elementos')),
                ('entEntregadoPor', models.CharField(db_comment='Nombre persona que entrega los materiales', max_length=100)),
                ('entObservaciones', models.TextField(db_comment='Observaciones que se requieran hacer', null=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('entProveedor', models.ForeignKey(db_comment='Hace referencia al proveedor que entrea los materiales', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.proveedor')),
                ('entUsuarioRecibe', models.ForeignKey(db_comment='Hace referencia a usuario de construcción que recibe', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Devolutivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('devPlacaSena', models.CharField(db_comment='Código Inventario SENA', max_length=45, unique=True)),
                ('devSerial', models.CharField(db_comment='Seríal del elemento devolutivo', max_length=45, null=True)),
                ('devDescripcion', models.TextField(db_comment='Descripción del elemento devolutivo')),
                ('devMarca', models.CharField(db_comment='Marca del Elemento Devolutivo', max_length=50, null=True)),
                ('devFechaIngresoSENA', models.DateField(db_comment='Fecha de ingreso del elemento al inventario SENA')),
                ('devValor', models.DecimalField(db_comment='Valor del elemento registrado inventario SENA', decimal_places=2, max_digits=11)),
                ('devFoto', models.FileField(blank=True, db_comment='Foto del Elemento Devolutivo', null=True, upload_to='elementos/')),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('devElemento', models.ForeignKey(db_comment='Hace relación al elemento FK', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.elemento')),
            ],
        ),
        migrations.CreateModel(
            name='DevolucionElemento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('devCantidadDevolucion', models.IntegerField(db_comment='Cantidad devuelta por el instructor después                                     de utilizarla en la formación')),
                ('devObservaciones', models.TextField(db_comment='Observaciones que el asistente quiera                                     agregar en la devolución', null=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('devSalida', models.ForeignKey(db_comment='Hace referencia a la salida de los elementos', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.salidadetallesolicitud')),
                ('devUsuario', models.ForeignKey(db_comment='Usuario que hace la devolución de elementos', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='detElemento',
            field=models.ForeignKey(db_comment='Elemento que se está solicitando', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.elemento'),
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='detSolicitud',
            field=models.ForeignKey(db_comment='Hace referencia a la solicitud del detalle que se va a registrar', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.solicitudelemento'),
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='detUnidadMedida',
            field=models.ForeignKey(db_comment='Unidad de médida del elemento que se requeire', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.unidadmedida'),
        ),
        migrations.CreateModel(
            name='DetalleEntradaMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detCantidad', models.IntegerField(db_comment='Cantidad que ingresa del material')),
                ('detPrecioUnitario', models.IntegerField(db_comment='Precio del material que ingresa')),
                ('devEstado', models.CharField(choices=[('Bueno', 'Bueno'), ('Bueno', 'Regular'), ('Bueno', 'Malo')], db_comment='estado del Elemento', max_length=7)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('detEntradaMaterial', models.ForeignKey(db_comment='Hace referencia a la Entrada registrada', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.entradamaterial')),
                ('detMaterial', models.ForeignKey(db_comment='Hace referencia al material que se está registrando en la entrada', on_delete=django.db.models.deletion.PROTECT, to='appGestionInventario.material')),
            ],
        ),
    ]
