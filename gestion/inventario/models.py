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

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=150)
    ruc_nit = models.CharField(max_length=20, unique=True)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_empresa

class Producto(models.Model):
    codigo_sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    meses_garantia = models.IntegerField()

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )

    proveedores = models.ManyToManyField(
        Proveedor,
        through='Suministro',
        related_name='productos'
    )

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
    
class FichaTecnica(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='ficha_tecnica')
    especificaciones = models.TextField(help_text="Detalles técnicos, dimensiones, peso, consumo eléctrico, etc.")
    manual_usuario_url = models.URLField(max_length=255, blank=True, null=True, help_text="Enlace al manual o documentación digital")
    norma_certificacion = models.CharField(max_length=100, blank=True, null=True, help_text="Ejemplo: ISO 9001, CE, RoHS, etc.")
    fecha_revision = models.DateField(auto_now=True)

    def __str__(self):
        return f"Ficha Técnica - {self.producto.nombre}"




class Suministro(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    dias_entrega_promedio = models.IntegerField(help_text="Tiempo estimado de entrega en días")
    es_proveedor_principal = models.BooleanField(default=False)
    fecha_ultimo_pedido = models.DateField(auto_now=True)

    class Meta:
        # Evita duplicar el mismo proveedor para el mismo producto
        unique_together = ('producto', 'proveedor')

    def __str__(self):
        return f"{self.proveedor.nombre_empresa} -> {self.producto.nombre}"