# DesarrolloSistemasEmpresariales-Lab03

## Repositorio (Modo de entrega)
https://github.com/JDiegoGD/DesarrolloSistemasEmpresariales-Lab03

## Problematica:
##### Gestión ineficiente en la cadena de suministro y servicios postventa de una Empresa Distribuidora de Equipos Médicos.


## Usuarios Involucrados:
* Administrador del Sistema: Gestiona permisos, roles y configuraciones.
* Jefe de Inventario y Logística: Registra la entrada de lotes, control de existencias, ubicaciones en almacén y despachos.
* Asesor Comercial: Genera cotizaciones, registra clientes y formaliza las órdenes de venta.
* Técnico de Soporte: Registra los mantenimientos, diagnósticos y solicitudes de repuestos para los equipos instalados.
* Cliente: Accede a un portal para solicitar soporte, revisar el estado de los equipos y consultar facturas.

## Requisitos Funcionales del Sistema Web:
* **RF-01** Crear Producto en Catálogo - Crear: Permitir al Jefe de Inventario registrar nuevos equipos médicos, especificando datos obligatorios como SKU, nombre, marca, modelo y costo base.
* **RF-02** Registrar Cliente - Crear: El sistema debe permitir al Asesor Comercial registrar nuevos clientes (clínicas u hospitales), ingresando su RUC/NIT, razón social, dirección fiscal y datos de contacto.
* **RF-03** Apertura de Ticket de Soporte - Crear: El sistema debe permitir al Cliente o Técnico crear un ticket de incidencia técnica vinculando el número de serie del equipo afectado y detallando la falla reportada.
* **RF-04** Listar Equipos Instalados - Leer: El sistema debe permitir a los usuarios autorizados consultar un listado general de los equipos en servicio, incluyendo filtros por cliente, estado de garantía y rango de fechas.
* **RF-05** Consultar Panel de Tickets - Leer: Permitir al Técnico y al Cliente visualizar el estado de las solicitudes de mantenimiento activas, filtradas por prioridad o estado.
* **RF-06** Actualizar Datos del Cliente - Actualizar: Permitir al Administrador o Asesor Comercial modificar la información de contacto y ubicación de un cliente registrado.
* **RF-07** Actualizar Estado de Ticket - Actualizar: Permitir al Técnico de Soporte actualizar el estado del ticket, asignar diagnósticos y registrar repuestos utilizados.
* **RF-08** Inactivar Usuario o Registro - Eliminar: El sistema debe permitir al Administrador realizar la baja lógica (desactivación) de usuarios o clientes inactivos para impedir su acceso al sistema sin perder el historial operativo.

## Cobertura de Operaciones CRUD
* Crear (Create): RF-01, RF-02, RF-03
* Leer / Listar (Read): RF-04, RF-05
* Actualizar (Update): RF-06, RF-07
* Eliminar / Inactivar (Delete): RF-08

---


```python
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
```

## Representacion de Relaciones
* Entidades Independientes:
    * Clientes
    * Productos
    * Usuarios
    * Entidades Vinculadas (Relación 1:N):
    * Plaintext

* Entidad A: Clientes
* Entidad B: Productos
* Entidad C: Usuarios


### Explicación de la Relación:
* Un Cliente (Entidad D) puede poseer N Equipos_Instalados (Entidad E).
* Un Equipo_Instalado (Entidad E) pertenece obligatoriamente a 1 Cliente (Entidad D).


## Implementar READ
```
templates/
└── inventario/
    ├── base.html
    ├── crear_producto.html
    ├── lista_clientes.html
    ├── lista_equipos.html
    ├── lista_productos.html
    ├── lista_tickets.html
    └── lista_usuarios.html
```

## Implementar UPDATE
```
templates/
└── inventario/
    ├── base.html
    ├── crear_producto.html
    ├── editar_cliente.html
    ├── editar_equipo.html
    ├── editar_producto.html
    ├── editar_ticket.html
    ├── editar_usuario.html
    ├── lista_clientes.html
    ├── lista_equipos.html
    ├── lista_productos.html
    ├── lista_tickets.html
    └── lista_usuarios.html
```

## Implementar DELETE 



```
templates/
└── inventario/
    ├── eliminar_cliente.html
    ├── eliminar_equipo.html
    ├── eliminar_producto.html
    ├── eliminar_ticket.html
    └── eliminar_usuario.html
```

---


Relación elegida: **N:M con modelo intermedio** entre `Producto` y `Proveedor`, a través de `Suministro` (campos propios: `precio_compra`, `dias_entrega_promedio`, `es_proveedor_principal`, `fecha_ultimo_pedido`). Es la relación más completa de las tres (1:1, 1:N, N:M) porque obliga a atravesar una tabla puente en vez de una FK directa.

Caso de uso documentado: el usuario abre **"Productos & Proveedores"**, que renderiza `productos_proveedores.html` a partir de la vista `productos_proveedores`.

### Recorrido completo

```
1. Request  → GET /inventario/productos/proveedores/
2. URL      → gestion/urls.py enruta el prefijo "inventario/" a inventario/urls.py,
              que resuelve la ruta al view `productos_proveedores` (name="productos_proveedores")
3. View     → views.productos_proveedores(request) arma el queryset
4. ORM      → Producto.objects.prefetch_related('suministro_set__proveedor').order_by('nombre')
              (queryset LAZY: todavía no toca la base de datos)
5. SQLite   → Al evaluarse el queryset (paso 8) se disparan 3 SELECT (ver tabla más abajo)
6. View     → recibe el queryset ya resuelto en memoria (con las relaciones precargadas)
7. Context  → render(request, 'inventario/productos_proveedores.html', {'productos': productos})
8. Template → {% for producto in productos %} evalúa el queryset (dispara el SQL real)
              {% for suministro in producto.suministro_set.all %} recorre el modelo intermedio
              {{ suministro.proveedor.nombre_empresa }} accede al Proveedor final
9. Response → Django serializa el HTML resultante en un HttpResponse 200 (text/html)
```

### Operación SQL conceptual de cada acción ORM

| Acción ORM | SQL conceptual equivalente |
|---|---|
| `Producto.objects.order_by('nombre')` | `SELECT * FROM inventario_producto ORDER BY nombre ASC;` |
| `.prefetch_related('suministro_set')` | `SELECT * FROM inventario_suministro WHERE producto_id IN (<ids de la consulta anterior>);` (consulta separada, no `JOIN`) |
| `.prefetch_related('suministro_set__proveedor')` | `SELECT * FROM inventario_proveedor WHERE id IN (<proveedor_id de los suministros obtenidos>);` |
| `suministro.proveedor` (tras el prefetch) | Ninguna: ya está en caché de Python — sin esto sería `SELECT * FROM inventario_proveedor WHERE id = <proveedor_id>;` por cada fila |
| Alternativa con `select_related` (usada en `lista_productos` para `categoria`/`ficha_tecnica`) | `SELECT ... FROM inventario_producto INNER/LEFT JOIN inventario_categoria ON ... LEFT JOIN inventario_ficha_tecnica ON ...;` (una sola consulta con `JOIN`, apta para 1:1 y 1:N pero no para N:M porque duplicaría filas) |

### Observación técnica

En esta misma plantilla, `producto.categoria.nombre` **no** está en el `prefetch_related`/`select_related` de la vista `productos_proveedores`, por lo que cada fila dispara un `SELECT * FROM inventario_categoria WHERE id = <categoria_id>` adicional (patrón N+1). Es la comparación práctica de por qué `select_related`/`prefetch_related` existen: sin ellos, cada acceso a una relación desde el template genera una consulta nueva a SQLite.

---

## Modelo de Datos Ampliado (Entidades y Relaciones)

Sobre las 5 entidades originales de la Semana 3 (`Cliente`, `Producto`, `Usuario`, `EquipoInstalado`, `TicketSoporte`, vinculadas únicamente por Foreign Key) se incorporaron los tres tipos de relación exigidos, sumando 4 entidades nuevas: `Categoria`, `FichaTecnica`, `Proveedor` y `Suministro` (modelo intermedio). El modelo completo queda en 9 entidades.

### Entidades

| Entidad | Rol en el dominio |
|---|---|
| `Cliente` | Clínica/hospital que compra equipos y reporta soporte |
| `Producto` | Equipo médico del catálogo (entidad central del modelo) |
| `Usuario` | Personal interno del sistema (admin, ventas, logística, técnico) |
| `EquipoInstalado` | Instancia física de un `Producto` en las instalaciones de un `Cliente` |
| `TicketSoporte` | Incidencia técnica registrada sobre un `EquipoInstalado` |
| `Categoria` | Clasificación de `Producto` (ej. Refrigeración, Climatización) |
| `FichaTecnica` | Detalle técnico exclusivo de un `Producto` (dimensiones, certificaciones, manual) |
| `Proveedor` | Empresa externa que abastece `Producto` |
| `Suministro` | Modelo intermedio: qué `Proveedor` abastece qué `Producto` y en qué condiciones comerciales |

### Relaciones

| Relación | Tipo | Implementación Django | Acceso desde código/template |
|---|---|---|---|
| Categoria → Producto | 1:N | `Producto.categoria = ForeignKey(Categoria, on_delete=PROTECT, related_name='productos')` | Directo: `producto.categoria` · Inverso: `categoria.productos.all()` |
| Producto → FichaTecnica | 1:1 | `FichaTecnica.producto = OneToOneField(Producto, on_delete=CASCADE, related_name='ficha_tecnica')` | Directo: `producto.ficha_tecnica` |
| Producto ↔ Proveedor | N:M con modelo intermedio | `Producto.proveedores = ManyToManyField(Proveedor, through='Suministro', related_name='productos')` | `producto.suministro_set.all()` → `suministro.proveedor`, exponiendo además `precio_compra`, `dias_entrega_promedio`, `es_proveedor_principal`, `fecha_ultimo_pedido` |
| Producto → EquipoInstalado | 1:N (Semana 3) | `EquipoInstalado.producto = ForeignKey(Producto, on_delete=CASCADE, related_name='equipos')` | `producto.equipos.all()` |
| Cliente → EquipoInstalado | 1:N (Semana 3) | `EquipoInstalado.cliente = ForeignKey(Cliente, on_delete=CASCADE, related_name='equipos')` | `cliente.equipos.all()` |
| EquipoInstalado → TicketSoporte | 1:N (Semana 3) | `TicketSoporte.equipo = ForeignKey(EquipoInstalado, on_delete=CASCADE, related_name='tickets')` | `equipo.tickets.all()` |
| Usuario → TicketSoporte | 1:N (Semana 3) | `TicketSoporte.tecnico = ForeignKey(Usuario, on_delete=SET_NULL, null=True, related_name='tickets_asignados')` | `usuario.tickets_asignados.all()` |

### Integridad del modelo intermedio

`Suministro` define `unique_together = ('producto', 'proveedor')`: un mismo proveedor no puede registrarse dos veces para el mismo producto. Las vistas `crear_suministro` y `editar_suministro` capturan el `IntegrityError` resultante y lo devuelven como error de formulario legible en vez de un error 500.

### CRUD del modelo intermedio

Se implementó el CRUD completo de `Suministro` (agregar, editar y quitar un proveedor de un producto, con sus atributos propios), accesible desde "Productos & Proveedores":

```
templates/
└── inventario/
    ├── crear_suministro.html
    ├── editar_suministro.html
    └── eliminar_suministro.html
```

* `crear_suministro(request, producto_pk)` — crea un `Suministro` fijando el `Producto` por URL y seleccionando el `Proveedor` y sus condiciones (precio de compra, días de entrega, si es principal) en el formulario.
* `editar_suministro(request, pk)` — actualiza las condiciones comerciales de una relación producto-proveedor ya existente.
* `eliminar_suministro(request, pk)` — quita a un proveedor de un producto, con pantalla de confirmación previa.

### Dependencias (`requirements.txt`)

```
asgiref==3.12.1
Django==6.1.1
sqlparse==0.6.0
tzdata==2026.3
```

No se agregaron paquetes nuevos para la ampliación del modelo: los tres tipos de relación (1:1, 1:N, N:M) y el CRUD del modelo intermedio se resuelven con el ORM de Django incluido en la dependencia base.
