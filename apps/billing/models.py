import uuid

from django.db import models
from django.utils import timezone


class Garantia(models.Model):

    # ------------------------------------------------------------------
    # Choices
    # ------------------------------------------------------------------

    class Estado(models.TextChoices):
        NUEVA = "nueva", "Nueva"
        APROBADA = "aprobada", "Aprobada"
        CONTRATO_FIRMADO = "contrato_firmado", "Contrato de Fianza Firmado"
        DE_BAJA = "de_baja", "De Baja"

    class EstadoCivil(models.TextChoices):
        SOLTERO = "soltero", "Soltero/a"
        CASADO = "casado", "Casado/a"
        DIVORCIADO = "divorciado", "Divorciado/a"
        VIUDO = "viudo", "Viudo/a"
        UNION_CONVIVENCIAL = "union_convivencial", "Unión Convivencial"

    class TipoInmueble(models.TextChoices):
        DEPARTAMENTO = "departamento", "Departamento"
        CASA = "casa", "Casa"
        LOCAL_COMERCIAL = "local_comercial", "Local Comercial"
        OFICINA = "oficina", "Oficina"
        PH = "ph", "PH"

    class UsoInmueble(models.TextChoices):
        RESIDENCIAL = "residencial", "Residencial"
        COMERCIAL = "comercial", "Comercial"

    class MetodoPago(models.TextChoices):
        TRANSFERENCIA = "transferencia", "Transferencia Bancaria"
        EFECTIVO = "efectivo", "Efectivo"
        DEBITO_CREDITO = "debito_credito", "Débito / Crédito"
        MERCADOPAGO = "mercadopago", "MercadoPago"

    # ------------------------------------------------------------------
    # Identificación
    # ------------------------------------------------------------------

    numero_solicitud = models.CharField(
        "Nº de solicitud",
        max_length=20,
        unique=True,
        editable=False,
    )
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=Estado.choices,
        default=Estado.NUEVA,
    )

    # ------------------------------------------------------------------
    # Datos del solicitante
    # ------------------------------------------------------------------

    nombre = models.CharField("Nombre", max_length=100)
    apellido = models.CharField("Apellido", max_length=100)
    dni = models.CharField("DNI", max_length=10)
    fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
    email = models.EmailField("Email")
    telefono = models.CharField("Teléfono", max_length=20)
    domicilio_actual = models.CharField("Domicilio actual", max_length=255)
    estado_civil = models.CharField(
        "Estado civil",
        max_length=30,
        choices=EstadoCivil.choices,
        blank=True,
    )
    ocupacion = models.CharField("Ocupación", max_length=100, blank=True)
    ingreso_mensual = models.DecimalField(
        "Ingreso mensual",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Datos del inmueble
    # ------------------------------------------------------------------

    direccion_inmueble = models.CharField("Dirección del inmueble", max_length=255, blank=True)
    localidad = models.CharField("Localidad", max_length=100, blank=True)
    provincia = models.CharField("Provincia", max_length=100, blank=True)
    codigo_postal = models.CharField("Código postal", max_length=10, blank=True)
    tipo_inmueble = models.CharField(
        "Tipo de inmueble",
        max_length=20,
        choices=TipoInmueble.choices,
        blank=True,
    )
    uso_inmueble = models.CharField(
        "Uso del inmueble",
        max_length=20,
        choices=UsoInmueble.choices,
        blank=True,
    )
    monto_alquiler = models.DecimalField(
        "Monto de alquiler",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    duracion_contrato_meses = models.PositiveSmallIntegerField(
        "Duración del contrato (meses)",
        null=True,
        blank=True,
    )
    nombre_propietario = models.CharField("Nombre del propietario", max_length=200, blank=True)
    telefono_propietario = models.CharField("Teléfono del propietario", max_length=20, blank=True)

    # ------------------------------------------------------------------
    # Datos de pago
    # ------------------------------------------------------------------

    metodo_pago = models.CharField(
        "Método de pago",
        max_length=20,
        choices=MetodoPago.choices,
        blank=True,
    )
    monto_pagado = models.DecimalField(
        "Monto pagado",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    fecha_pago = models.DateField("Fecha de pago", null=True, blank=True)
    comprobante_numero = models.CharField("Nº de comprobante", max_length=100, blank=True)
    observaciones_pago = models.TextField("Observaciones de pago", blank=True)

    # ------------------------------------------------------------------
    # De baja
    # ------------------------------------------------------------------

    motivo_baja = models.TextField("Motivo de baja", blank=True)

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField("Última actualización", auto_now=True)
    fecha_aprobacion = models.DateTimeField("Fecha de aprobación", null=True, blank=True)
    fecha_firma_contrato = models.DateTimeField("Fecha de firma de contrato", null=True, blank=True)
    fecha_baja = models.DateTimeField("Fecha de baja", null=True, blank=True)

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"
        ordering = ["-fecha_creacion"]

    def __str__(self) -> str:
        return f"{self.numero_solicitud} — {self.apellido}, {self.nombre}"

    # ------------------------------------------------------------------
    # Lógica de negocio
    # ------------------------------------------------------------------

    def _tiene_datos_solicitante(self) -> bool:
        return all([self.nombre, self.apellido, self.dni, self.email, self.telefono, self.domicilio_actual])

    def _tiene_datos_inmueble(self) -> bool:
        return all([self.direccion_inmueble, self.localidad, self.provincia, self.tipo_inmueble, self.monto_alquiler])

    def _tiene_datos_pago(self) -> bool:
        return all([self.metodo_pago, self.monto_pagado, self.fecha_pago])

    def _calcular_estado_automatico(self) -> str:
        if self._tiene_datos_solicitante() and self._tiene_datos_inmueble() and self._tiene_datos_pago():
            return self.Estado.CONTRATO_FIRMADO
        if self._tiene_datos_solicitante() and self._tiene_datos_inmueble():
            return self.Estado.APROBADA
        return self.Estado.NUEVA

    def dar_de_baja(self, motivo: str = "") -> None:
        self.estado = self.Estado.DE_BAJA
        if motivo:
            self.motivo_baja = motivo
        if not self.fecha_baja:
            self.fecha_baja = timezone.now()
        self.save()

    def reactivar(self) -> None:
        self.estado = self._calcular_estado_automatico()
        self.fecha_baja = None
        self.save()

    def save(self, *args, **kwargs) -> None:
        if not self.numero_solicitud:
            self.numero_solicitud = f"GAR-{uuid.uuid4().hex[:8].upper()}"

        if self.estado != self.Estado.DE_BAJA:
            nuevo_estado = self._calcular_estado_automatico()
            now = timezone.now()

            if nuevo_estado == self.Estado.APROBADA and not self.fecha_aprobacion:
                self.fecha_aprobacion = now
            elif nuevo_estado == self.Estado.CONTRATO_FIRMADO and not self.fecha_firma_contrato:
                self.fecha_firma_contrato = now

            self.estado = nuevo_estado
            self.fecha_baja = None
        else:
            if not self.fecha_baja:
                self.fecha_baja = timezone.now()

        super().save(*args, **kwargs)
