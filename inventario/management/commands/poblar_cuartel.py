from django.core.management.base import BaseCommand
from inventario.models import Sitio, UnidadMovil, Herramienta


SITIOS = [
    {
        "nombre": "Cuartel Central",
        "localidad": "Ayacucho",
        "dotacion": 50,
        "descripcion": "Base principal del cuartel. 50 bomberos activos y curso de ingreso en formación.",
    },
    {
        "nombre": "Destacamento N° 1",
        "localidad": "Udaquiola",
        "dotacion": 12,
        "descripcion": "Destacamento descentralizado con dotación que incluye personal femenino.",
    },
]

# Sitio, denominación, tipo/función, función detallada, modelo, personal, agua (L), equipamiento
UNIDADES = [
    # ---- CUARTEL CENTRAL (Ayacucho) ----
    {
        "sitio": "Cuartel Central", "nombre": "Unidad 1",
        "clasificacion": "primera_salida",
        "funcion": "Primera salida: incendios estructurales y rescate vehicular urbano.",
        "modelo": "Mercedes-Benz 1620", "capacidad_personal": 6, "capacidad_agua": 3500,
        "equipamiento": "Bomba Rosenbauer de alta y baja presión; mangueras y devanaderas; equipamiento completo para incendios estructurales (EPIs, ERA); herramientas de corte y rescate vehicular básico.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unidad 17",
        "clasificacion": "rescate_vehicular",
        "funcion": "Rescate vehicular pesado en rutas.",
        "modelo": "Freightliner", "capacidad_personal": 6, "capacidad_agua": None,
        "equipamiento": "Herramientas hidráulicas pesadas de corte, expansión y elevación (tijeras, separadores, rams); tablas espinales y collarines de inmovilización; maletines y equipos de trauma.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unidad Forestal",
        "clasificacion": "forestal",
        "funcion": "Incendios forestales / pastizales. Ataque rápido.",
        "modelo": "Ford (tracción 4x4)", "capacidad_personal": 5, "capacidad_agua": 800,
        "equipamiento": "Kit de ataque rápido; motobomba de alta presión.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unidad 18",
        "clasificacion": "escalera",
        "funcion": "Incendios estructurales, ascenso y descenso en altura.",
        "modelo": "Pierce (Escalera Americana)", "capacidad_personal": None, "capacidad_agua": 3500,
        "equipamiento": "Escalera telescópica de 25 metros; bomba de agua de alto caudal; monitores / pitones de alto flujo.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unidad 8",
        "clasificacion": "utilitario",
        "funcion": "Apoyo y traslado de personal.",
        "modelo": "Chevrolet S10", "capacidad_personal": 4, "capacidad_agua": None,
        "equipamiento": "Apoyo logístico a la Unidad 1 en incendios estructurales.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unidad 6",
        "clasificacion": "rescate_vehicular",
        "funcion": "Rescate vehicular y estructural. Apoyo a la Unidad 17.",
        "modelo": "", "capacidad_personal": None, "capacidad_agua": None,
        "equipamiento": "Herramientas de rescate vehicular y herramientas de entrada forzada / estructural.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unidad Forestal (Astra)",
        "clasificacion": "forestal",
        "funcion": "Incendios forestales de gran escala.",
        "modelo": "Iveco Astra", "capacidad_personal": 6, "capacidad_agua": 6000,
        "equipamiento": "Bomba de gran volumen y equipamiento de zapa / forestal.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unimog",
        "clasificacion": "forestal",
        "funcion": "Incendios forestales / terrenos difíciles.",
        "modelo": "Mercedes-Benz Unimog (4x4)", "capacidad_personal": 3, "capacidad_agua": 100,
        "equipamiento": "Motobomba independiente (no cardánica) que permite lanzar agua en movimiento; devanadera de alta presión operada desde la parte superior; escalera manual de techo.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Peugeot Expert",
        "clasificacion": "utilitario",
        "funcion": "Utilitario: traslado de personal y viajes institucionales.",
        "modelo": "Peugeot Expert", "capacidad_personal": 6, "capacidad_agua": None,
        "equipamiento": "",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Unidad 15 (Cisterna)",
        "clasificacion": "cisterna",
        "funcion": "Abastecimiento de agua / recurso hídrico.",
        "modelo": "Iveco (tractor con semirremolque tanque)", "capacidad_personal": None, "capacidad_agua": 14000,
        "equipamiento": "Pileta de lona portátil (tanque de colapso) para descarga rápida en terreno y reaprovisionamiento de autobombas; mangas y acoples de gran diámetro.",
    },
    {
        "sitio": "Cuartel Central", "nombre": "Remolque / Motor Compresor",
        "clasificacion": "especial",
        "funcion": "Limpieza de rutas / trabajos de aire.",
        "modelo": "Compresor de alto rendimiento (origen alemán)", "capacidad_personal": None, "capacidad_agua": None,
        "equipamiento": "Sistema de sopleteo por aire a presión (barrido de semillas / grano o despojos en la calzada); bomba accionada por aire con caudal de 5.000 L/hora.",
    },
    # ---- DESTACAMENTO N° 1 (Udaquiola) ----
    {
        "sitio": "Destacamento N° 1", "nombre": "Unidad 25",
        "clasificacion": "forestal",
        "funcion": "Forestal / híbrido: rescate y pastizales.",
        "modelo": "Ford 4000 (4x4)", "capacidad_personal": None, "capacidad_agua": None,
        "equipamiento": "Tanque forestal; kit de extinción forestal y material básico de rescate.",
    },
    {
        "sitio": "Destacamento N° 1", "nombre": "Unidad 14",
        "clasificacion": "utilitario",
        "funcion": "Transporte de personal.",
        "modelo": "", "capacidad_personal": None, "capacidad_agua": None,
        "equipamiento": "",
    },
    {
        "sitio": "Destacamento N° 1", "nombre": "Camión GMC",
        "clasificacion": "forestal",
        "funcion": "Forestal / rescate.",
        "modelo": "GMC 6 cilindros (origen americano)", "capacidad_personal": None, "capacidad_agua": None,
        "equipamiento": "Herramientas de rescate vehicular y equipo forestal.",
    },
    {
        "sitio": "Destacamento N° 1", "nombre": "Unidad 16",
        "clasificacion": "utilitario",
        "funcion": "Logística y transporte en caminos rurales.",
        "modelo": "Chevrolet LUV (4x4)", "capacidad_personal": None, "capacidad_agua": None,
        "equipamiento": "",
    },
    {
        "sitio": "Destacamento N° 1", "nombre": "Unidad 21 (Ambulancia)",
        "clasificacion": "ambulancia",
        "funcion": "Rescate, soporte vital y traslado sanitario.",
        "modelo": "", "capacidad_personal": None, "capacidad_agua": None,
        "equipamiento": "Camilla de traslado; tubos de oxígeno; kits de inmovilización (chalecos, collarines, tablas); maletines de primeros auxilios y atención de trauma.",
    },
    {
        "sitio": "Destacamento N° 1", "nombre": "Unidad de Salida Rápida",
        "clasificacion": "forestal",
        "funcion": "Ataque rápido.",
        "modelo": "", "capacidad_personal": None, "capacidad_agua": 2500,
        "equipamiento": "",
    },
]

# codigo, nombre, ubicacion, unidad móvil (nombre)
HERRAMIENTAS = [
    # ---- Unidad 1 ----
    {"codigo": "#101", "nombre": "ERA completo (Equipo de Respiración Autónoma)", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#102", "nombre": "Máscara de repuesto para ERA", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#103", "nombre": "Tramo de línea 45mm (sintética)", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#104", "nombre": "Tramo de línea 63mm (sintética)", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#105", "nombre": "Devanadera con manguera blindada", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#106", "nombre": "Lanza / pitón regulable de caudal", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#107", "nombre": "Lanza tipo Pocket (ataque rápido)", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#108", "nombre": "EPI estructural completo (buzo, casco, guantes, botas)", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#109", "nombre": "Hacha de dotación", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#110", "nombre": "Barra Halligan (entrada forzada)", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#111", "nombre": "Linterna de pecho anti-explosiva", "ubicacion": "estructural", "unidad": "Unidad 1"},
    {"codigo": "#112", "nombre": "Kit básico de corte y rescate vehicular", "ubicacion": "rescate", "unidad": "Unidad 1"},
    # ---- Unidad 17 ----
    {"codigo": "#113", "nombre": "Tijera hidráulica de corte", "ubicacion": "rescate", "unidad": "Unidad 17"},
    {"codigo": "#114", "nombre": "Separador / expansor hidráulico", "ubicacion": "rescate", "unidad": "Unidad 17"},
    {"codigo": "#115", "nombre": "Ram / cilindro de elevación hidráulico", "ubicacion": "rescate", "unidad": "Unidad 17"},
    {"codigo": "#116", "nombre": "Central hidráulica de accionamiento", "ubicacion": "rescate", "unidad": "Unidad 17"},
    {"codigo": "#117", "nombre": "Tabla espinal larga", "ubicacion": "rescate", "unidad": "Unidad 17"},
    {"codigo": "#118", "nombre": "Collarines de inmovilización cervical (set)", "ubicacion": "rescate", "unidad": "Unidad 17"},
    {"codigo": "#119", "nombre": "Maletín de trauma / atención prehospitalaria", "ubicacion": "rescate", "unidad": "Unidad 17"},
    # ---- Unidad Forestal ----
    {"codigo": "#120", "nombre": "Kit de ataque rápido forestal", "ubicacion": "forestal", "unidad": "Unidad Forestal"},
    {"codigo": "#121", "nombre": "Motobomba de alta presión", "ubicacion": "forestal", "unidad": "Unidad Forestal"},
    {"codigo": "#122", "nombre": "Devanadera de alta presión (manguera)", "ubicacion": "forestal", "unidad": "Unidad Forestal"},
    # ---- Unidad 18 ----
    {"codigo": "#123", "nombre": "Monitor / pitón de alto flujo", "ubicacion": "estructural", "unidad": "Unidad 18"},
    {"codigo": "#124", "nombre": "Arnés y equipo de trabajo en altura", "ubicacion": "estructural", "unidad": "Unidad 18"},
    # ---- Unidad 6 ----
    {"codigo": "#125", "nombre": "Set de entrada forzada estructural", "ubicacion": "estructural", "unidad": "Unidad 6"},
    {"codigo": "#126", "nombre": "Herramientas manuales de rescate vehicular", "ubicacion": "rescate", "unidad": "Unidad 6"},
    # ---- Astra ----
    {"codigo": "#127", "nombre": "Equipamiento de zapa / forestal (batefuegos, palas)", "ubicacion": "forestal", "unidad": "Unidad Forestal (Astra)"},
    {"codigo": "#128", "nombre": "Mochila forestal / porra de agua", "ubicacion": "forestal", "unidad": "Unidad Forestal (Astra)"},
    # ---- Unimog ----
    {"codigo": "#129", "nombre": "Devanadera de alta presión superior", "ubicacion": "forestal", "unidad": "Unimog"},
    {"codigo": "#130", "nombre": "Escalera manual de techo", "ubicacion": "forestal", "unidad": "Unimog"},
    {"codigo": "#131", "nombre": "Motobomba independiente (no cardánica)", "ubicacion": "forestal", "unidad": "Unimog"},
    # ---- Unidad 15 (Cisterna) ----
    {"codigo": "#132", "nombre": "Pileta de lona portátil (tanque de colapso)", "ubicacion": "cisterna", "unidad": "Unidad 15 (Cisterna)"},
    {"codigo": "#133", "nombre": "Mangas de gran diámetro (abastecimiento)", "ubicacion": "cisterna", "unidad": "Unidad 15 (Cisterna)"},
    {"codigo": "#134", "nombre": "Acoples de gran diámetro", "ubicacion": "cisterna", "unidad": "Unidad 15 (Cisterna)"},
    # ---- Destacamento: Unidad 25 ----
    {"codigo": "#135", "nombre": "Kit de extinción forestal", "ubicacion": "forestal", "unidad": "Unidad 25"},
    {"codigo": "#136", "nombre": "Material básico de rescate", "ubicacion": "rescate", "unidad": "Unidad 25"},
    # ---- Destacamento: Camión GMC ----
    {"codigo": "#137", "nombre": "Herramientas manuales de rescate vehicular", "ubicacion": "rescate", "unidad": "Camión GMC"},
    {"codigo": "#138", "nombre": "Equipo forestal (batefuegos, mochila)", "ubicacion": "forestal", "unidad": "Camión GMC"},
    # ---- Destacamento: Ambulancia 21 ----
    {"codigo": "#139", "nombre": "Camilla de traslado", "ubicacion": "rescate", "unidad": "Unidad 21 (Ambulancia)"},
    {"codigo": "#140", "nombre": "Tubos de oxígeno (set)", "ubicacion": "rescate", "unidad": "Unidad 21 (Ambulancia)"},
    {"codigo": "#141", "nombre": "Kits de inmovilización (chalecos, collarines, tablas)", "ubicacion": "rescate", "unidad": "Unidad 21 (Ambulancia)"},
    {"codigo": "#142", "nombre": "Maletines de primeros auxilios / trauma", "ubicacion": "rescate", "unidad": "Unidad 21 (Ambulancia)"},
    # ---- Herramientas adicionales (depósito / únicas) ----
    {"codigo": "#005", "nombre": "Boquilla de acople rápido (Varias medidas)", "ubicacion": "estructural"},
    {"codigo": "#008", "nombre": "Tanque de oxígeno de repuesto (Carga completa)", "ubicacion": "estructural"},
    {"codigo": "#015", "nombre": "Motosierra para ventilación estructural", "ubicacion": "rescate"},
    {"codigo": "#016", "nombre": "Kit de tacos y escalonados de estabilización", "ubicacion": "rescate"},
    {"codigo": "#017", "nombre": "Linterna de escena portátil (Reflector)", "ubicacion": "rescate"},
    {"codigo": "#021", "nombre": "Maletín de oxigenoterapia medicinal", "ubicacion": "rescate"},
    {"codigo": "#022", "nombre": "Kit de férulas de inmovilización", "ubicacion": "rescate"},
    {"codigo": "#023", "nombre": "Desfibrilador Externo Automático (DEA)", "ubicacion": "rescate"},
    {"codigo": "#024", "nombre": "Hacha-pala Pulaski", "ubicacion": "forestal"},
    {"codigo": "#025", "nombre": "Rastrillo segador McLeod", "ubicacion": "forestal"},
    {"codigo": "#026", "nombre": "Pala forestal de punta", "ubicacion": "forestal"},
    {"codigo": "#027", "nombre": "Batefuegos forestal de goma", "ubicacion": "forestal"},
    {"codigo": "#028", "nombre": "Mochila de agua para extinción (20L)", "ubicacion": "forestal", "estado": "En Reparación", "disponibilidad": "No Disponible"},
    {"codigo": "#030", "nombre": "Tramo de línea forestal 25mm", "ubicacion": "forestal"},
    {"codigo": "#031", "nombre": "Tramo de línea 63mm (Abastecimiento)", "ubicacion": "cisterna"},
    {"codigo": "#032", "nombre": "Kit de acoples rápidos y reducciones de rosca", "ubicacion": "cisterna"},
    {"codigo": "#033", "nombre": "Motobomba de llenado rápido de alta capacidad", "ubicacion": "cisterna"},
    {"codigo": "#034", "nombre": "Mangote de succión para fuentes abiertas", "ubicacion": "cisterna"},
    {"codigo": "#035", "nombre": "Llave de paso para hidrante", "ubicacion": "cisterna"},
    {"codigo": "#036", "nombre": "Bidón de líquido espumógeno (AFFF 3%)", "ubicacion": "deposito"},
    {"codigo": "#038", "nombre": "Bidón de mezcla combustible para 2 tiempos", "ubicacion": "deposito"},
]


class Command(BaseCommand):
    help = "Carga todos los datos del cuartel: sitios, unidades móviles y el inventario completo de herramientas (por unidad, depósito y extras)."

    def handle(self, *args, **options):
        creados_sitios = 0
        actualizados_sitios = 0
        sitios = {}

        for s in SITIOS:
            sitio, creado = Sitio.objects.update_or_create(
                nombre=s["nombre"],
                defaults={
                    "localidad": s["localidad"],
                    "dotacion": s["dotacion"],
                    "descripcion": s["descripcion"],
                },
            )
            sitios[s["nombre"]] = sitio
            if creado:
                creados_sitios += 1
            else:
                actualizados_sitios += 1

        creados_unidades = 0
        actualizados_unidades = 0
        unidades = {}

        for u in UNIDADES:
            sitio = sitios[u["sitio"]]
            unidad, creado = UnidadMovil.objects.update_or_create(
                sitio=sitio,
                nombre=u["nombre"],
                defaults={
                    "clasificacion": u["clasificacion"],
                    "funcion": u["funcion"],
                    "modelo": u["modelo"],
                    "capacidad_personal": u["capacidad_personal"],
                    "capacidad_agua": u["capacidad_agua"],
                    "equipamiento": u["equipamiento"],
                },
            )
            unidades[u["nombre"]] = unidad
            if creado:
                creados_unidades += 1
            else:
                actualizados_unidades += 1

        creados_herramientas = 0
        actualizados_herramientas = 0

        for h in HERRAMIENTAS:
            unidad = unidades.get(h.get("unidad"))
            herramienta, creado = Herramienta.objects.update_or_create(
                codigo=h["codigo"],
                defaults={
                    "nombre": h["nombre"],
                    "ubicacion": h["ubicacion"],
                    "unidad": unidad,
                    "estado": h.get("estado", "Funcional"),
                    "disponibilidad": h.get("disponibilidad", "Disponible"),
                },
            )
            if creado:
                creados_herramientas += 1
            else:
                actualizados_herramientas += 1

        self.stdout.write("==========================================")
        self.stdout.write(self.style.SUCCESS("[OK] Población de cuartel completada exitosamente!"))
        self.stdout.write(f"Sitios creados: {creados_sitios} | actualizados: {actualizados_sitios}")
        self.stdout.write(f"Unidades creadas: {creados_unidades} | actualizadas: {actualizados_unidades}")
        self.stdout.write(f"Herramientas creadas: {creados_herramientas} | actualizadas: {actualizados_herramientas}")
        self.stdout.write("==========================================")
