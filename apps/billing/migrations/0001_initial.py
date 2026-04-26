import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Garantia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero_solicitud", models.CharField(editable=False, max_length=20, unique=True, verbose_name="Nº de solicitud")),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("nueva", "Nueva"),
                            ("aprobada", "Aprobada"),
                            ("contrato_firmado", "Contrato de Fianza Firmado"),
                            ("de_baja", "De Baja"),
                        ],
                        default="nueva",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                # Datos del solicitante
                ("nombre", models.CharField(max_length=100, verbose_name="Nombre")),
                ("apellido", models.CharField(max_length=100, verbose_name="Apellido")),
                ("dni", models.CharField(max_length=10, verbose_name="DNI")),
                ("fecha_nacimiento", models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("telefono", models.CharField(max_length=20, verbose_name="Teléfono")),
                ("domicilio_actual", models.CharField(max_length=255, verbose_name="Domicilio actual")),
                (
                    "estado_civil",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("soltero", "Soltero/a"),
                            ("casado", "Casado/a"),
                            ("divorciado", "Divorciado/a"),
                            ("viudo", "Viudo/a"),
                            ("union_convivencial", "Unión Convivencial"),
                        ],
                        max_length=30,
                        verbose_name="Estado civil",
                    ),
                ),
                ("ocupacion", models.CharField(blank=True, max_length=100, verbose_name="Ocupación")),
                ("ingreso_mensual", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name="Ingreso mensual")),
                # Datos del inmueble
                ("direccion_inmueble", models.CharField(blank=True, max_length=255, verbose_name="Dirección del inmueble")),
                ("localidad", models.CharField(blank=True, max_length=100, verbose_name="Localidad")),
                ("provincia", models.CharField(blank=True, max_length=100, verbose_name="Provincia")),
                ("codigo_postal", models.CharField(blank=True, max_length=10, verbose_name="Código postal")),
                (
                    "tipo_inmueble",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("departamento", "Departamento"),
                            ("casa", "Casa"),
                            ("local_comercial", "Local Comercial"),
                            ("oficina", "Oficina"),
                            ("ph", "PH"),
                        ],
                        max_length=20,
                        verbose_name="Tipo de inmueble",
                    ),
                ),
                (
                    "uso_inmueble",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("residencial", "Residencial"),
                            ("comercial", "Comercial"),
                        ],
                        max_length=20,
                        verbose_name="Uso del inmueble",
                    ),
                ),
                ("monto_alquiler", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name="Monto de alquiler")),
                ("duracion_contrato_meses", models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Duración del contrato (meses)")),
                ("nombre_propietario", models.CharField(blank=True, max_length=200, verbose_name="Nombre del propietario")),
                ("telefono_propietario", models.CharField(blank=True, max_length=20, verbose_name="Teléfono del propietario")),
                # Datos de pago
                (
                    "metodo_pago",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("transferencia", "Transferencia Bancaria"),
                            ("efectivo", "Efectivo"),
                            ("debito_credito", "Débito / Crédito"),
                            ("mercadopago", "MercadoPago"),
                        ],
                        max_length=20,
                        verbose_name="Método de pago",
                    ),
                ),
                ("monto_pagado", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name="Monto pagado")),
                ("fecha_pago", models.DateField(blank=True, null=True, verbose_name="Fecha de pago")),
                ("comprobante_numero", models.CharField(blank=True, max_length=100, verbose_name="Nº de comprobante")),
                ("observaciones_pago", models.TextField(blank=True, verbose_name="Observaciones de pago")),
                # De baja
                ("motivo_baja", models.TextField(blank=True, verbose_name="Motivo de baja")),
                # Timestamps
                ("fecha_creacion", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("fecha_actualizacion", models.DateTimeField(auto_now=True, verbose_name="Última actualización")),
                ("fecha_aprobacion", models.DateTimeField(blank=True, null=True, verbose_name="Fecha de aprobación")),
                ("fecha_firma_contrato", models.DateTimeField(blank=True, null=True, verbose_name="Fecha de firma de contrato")),
                ("fecha_baja", models.DateTimeField(blank=True, null=True, verbose_name="Fecha de baja")),
            ],
            options={
                "verbose_name": "Garantía",
                "verbose_name_plural": "Garantías",
                "ordering": ["-fecha_creacion"],
            },
        ),
    ]
