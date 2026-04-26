from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Garantia

# ---------------------------------------------------------------------------
# Colores por estado
# ---------------------------------------------------------------------------

_ESTADO_COLORS = {
    Garantia.Estado.NUEVA: ("#1565C0", "#E3F2FD"),
    Garantia.Estado.APROBADA: ("#2E7D32", "#E8F5E9"),
    Garantia.Estado.CONTRATO_FIRMADO: ("#6A1B9A", "#F3E5F5"),
    Garantia.Estado.DE_BAJA: ("#B71C1C", "#FFEBEE"),
}


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):

    # ------------------------------------------------------------------
    # Listado
    # ------------------------------------------------------------------

    list_display = [
        "numero_solicitud",
        "nombre_completo",
        "estado_badge",
        "tipo_inmueble",
        "monto_alquiler_fmt",
        "localidad",
        "fecha_creacion",
    ]
    list_filter = ["estado", "tipo_inmueble", "uso_inmueble", "metodo_pago", "provincia"]
    search_fields = ["numero_solicitud", "nombre", "apellido", "dni", "direccion_inmueble"]
    date_hierarchy = "fecha_creacion"
    list_per_page = 25

    # ------------------------------------------------------------------
    # Detalle
    # ------------------------------------------------------------------

    readonly_fields = [
        "numero_solicitud",
        "estado",
        "fecha_creacion",
        "fecha_actualizacion",
        "fecha_aprobacion",
        "fecha_firma_contrato",
        "fecha_baja",
        "estado_badge",
        "progreso_completitud",
    ]

    fieldsets = (
        (
            "Estado de la solicitud",
            {
                "fields": (
                    ("numero_solicitud", "estado_badge"),
                    ("fecha_creacion", "fecha_actualizacion"),
                    ("fecha_aprobacion", "fecha_firma_contrato", "fecha_baja"),
                    "progreso_completitud",
                    "motivo_baja",
                ),
            },
        ),
        (
            "1 · Datos del solicitante",
            {
                "fields": (
                    ("nombre", "apellido"),
                    ("dni", "fecha_nacimiento"),
                    ("email", "telefono"),
                    "domicilio_actual",
                    ("estado_civil", "ocupacion"),
                    "ingreso_mensual",
                ),
            },
        ),
        (
            "2 · Datos del inmueble",
            {
                "fields": (
                    "direccion_inmueble",
                    ("localidad", "provincia", "codigo_postal"),
                    ("tipo_inmueble", "uso_inmueble"),
                    ("monto_alquiler", "duracion_contrato_meses"),
                    ("nombre_propietario", "telefono_propietario"),
                ),
            },
        ),
        (
            "3 · Datos de pago",
            {
                "fields": (
                    "metodo_pago",
                    ("monto_pagado", "fecha_pago"),
                    "comprobante_numero",
                    "observaciones_pago",
                ),
            },
        ),
    )

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    actions = ["action_dar_de_baja", "action_reactivar"]

    @admin.action(description="Dar de baja las garantías seleccionadas")
    def action_dar_de_baja(self, request, queryset):
        activas = queryset.exclude(estado=Garantia.Estado.DE_BAJA)
        count = activas.count()
        for garantia in activas:
            garantia.dar_de_baja()
        self.message_user(
            request,
            f"{count} garantía(s) marcada(s) como De Baja.",
            messages.WARNING,
        )

    @admin.action(description="Reactivar las garantías seleccionadas")
    def action_reactivar(self, request, queryset):
        bajas = queryset.filter(estado=Garantia.Estado.DE_BAJA)
        count = bajas.count()
        for garantia in bajas:
            garantia.reactivar()
        self.message_user(
            request,
            f"{count} garantía(s) reactivada(s).",
            messages.SUCCESS,
        )

    # ------------------------------------------------------------------
    # Campos calculados para el listado
    # ------------------------------------------------------------------

    @admin.display(description="Solicitante", ordering="apellido")
    def nombre_completo(self, obj: Garantia) -> str:
        return f"{obj.apellido}, {obj.nombre}" if obj.apellido else obj.nombre

    @admin.display(description="Estado", ordering="estado")
    def estado_badge(self, obj: Garantia) -> str:
        color, bg = _ESTADO_COLORS.get(obj.estado, ("#424242", "#F5F5F5"))
        return format_html(
            '<span style="'
            "background:{bg};"
            "color:{color};"
            "padding:3px 10px;"
            "border-radius:12px;"
            "font-size:0.82em;"
            "font-weight:600;"
            "white-space:nowrap;"
            '">{label}</span>',
            bg=bg,
            color=color,
            label=obj.get_estado_display(),
        )

    @admin.display(description="Alquiler", ordering="monto_alquiler")
    def monto_alquiler_fmt(self, obj: Garantia) -> str:
        if obj.monto_alquiler is None:
            return "—"
        return f"$ {obj.monto_alquiler:,.2f}"

    @admin.display(description="Completitud")
    def progreso_completitud(self, obj: Garantia) -> str:
        pasos = [
            ("Solicitante", obj._tiene_datos_solicitante()),
            ("Inmueble", obj._tiene_datos_inmueble()),
            ("Pago", obj._tiene_datos_pago()),
        ]
        items_html = "".join(
            format_html(
                '<span style="'
                "margin-right:8px;"
                "color:{color};"
                "font-weight:600;"
                '">{icon} {label}</span>',
                color="#2E7D32" if ok else "#9E9E9E",
                icon="✔" if ok else "○",
                label=label,
            )
            for label, ok in pasos
        )
        return format_html("<div>{}</div>", items_html)

    # ------------------------------------------------------------------
    # Títulos del site
    # ------------------------------------------------------------------

    def get_queryset(self, request):
        return super().get_queryset(request).defer("observaciones_pago")


# ---------------------------------------------------------------------------
# Personalización global del admin
# ---------------------------------------------------------------------------

admin.site.site_header = "Finaer · Panel de Administración"
admin.site.site_title = "Finaer Admin"
admin.site.index_title = "Gestión de garantías de alquiler"
