from django.db import models


class Cliente(models.Model):
    razon_social = models.CharField(max_length=150)
    numero_identificacion = models.CharField(max_length=20, unique=True)
    email_contacto = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion_fiscal = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.razon_social


class Producto(models.Model):
    codigo_sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    meses_garantia = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"


class Usuario(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('VENTAS', 'Asesor Comercial'),
        ('LOGISTICA', 'Jefe de Inventario'),
        ('TECNICO', 'Técnico de Soporte'),
    ]
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"


class EquipoInstalado(models.Model):
    ESTADOS = [
        ('OPERATIVO', 'Operativo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('INACTIVO', 'Inactivo'),
    ]
    numero_serie = models.CharField(max_length=100, unique=True)
    fecha_instalacion = models.DateField()
    fin_garantia = models.DateField()
    estado = models.CharField(max_length=30, choices=ESTADOS, default='OPERATIVO')
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='equipos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='equipos')

    def __str__(self):
        return f"Serie: {self.numero_serie} - {self.cliente.razon_social}"


class TicketSoporte(models.Model):
    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    ESTADOS = [
        ('ABIERTO', 'Abierto'),
        ('EN_PROCESO', 'En Proceso'),
        ('RESUELTO', 'Resuelto'),
        ('CERRADO', 'Cerrado'),
    ]
    codigo_ticket = models.CharField(max_length=20, unique=True)
    descripcion_falla = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='MEDIA')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    equipo = models.ForeignKey(EquipoInstalado, on_delete=models.CASCADE, related_name='tickets')
    tecnico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')

    def __str__(self):
        return f"{self.codigo_ticket} - {self.estado}"