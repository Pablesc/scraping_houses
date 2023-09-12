import scrapy
class ScrapingHousesItem(scrapy.Item):
    # define the fields for your item here like:
    precio = scrapy.Field()
    barrio = scrapy.Field()
    region = scrapy.Field()
    comuna = scrapy.Field()
    direccion = scrapy.Field()
    publicacion = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    ubicacion = scrapy.Field()
    superficie_total = scrapy.Field()
    superficie_util = scrapy.Field()
    dormitorios = scrapy.Field()
    banos = scrapy.Field()
    estacionamientos = scrapy.Field()
    bodegas = scrapy.Field()
    cantidad_de_pisos = scrapy.Field()
    tipo_de_casa = scrapy.Field()
    orientacion = scrapy.Field()
    antiguedad = scrapy.Field()
    gastos_comunes = scrapy.Field()
    alarma = scrapy.Field()
    conserjeria = scrapy.Field()
    porton_automatico = scrapy.Field()
    tipo_de_seguridad = scrapy.Field()
    con_condominio_cerrado = scrapy.Field()
    acceso_controlado = scrapy.Field()
    quincho = scrapy.Field()
    piscina = scrapy.Field()
    closets = scrapy.Field()
    bano_de_visitas = scrapy.Field()
    terraza = scrapy.Field()
    comedor = scrapy.Field()
    walk_in_closet = scrapy.Field()
    homeoffice = scrapy.Field()
    living = scrapy.Field()
    patio = scrapy.Field()
    dormitorio_en_suite = scrapy.Field()
    balcon = scrapy.Field()
    mansarda = scrapy.Field()
    jardin = scrapy.Field()
    cocina = scrapy.Field()
    dormitorio_y_bano_de_servicio = scrapy.Field()
    playroom = scrapy.Field()
    logia = scrapy.Field()
    desayunador = scrapy.Field()
    acceso_a_internet = scrapy.Field()
    aire_acondicionado = scrapy.Field()
    calefaccion = scrapy.Field()
    tv_por_cable = scrapy.Field()
    linea_telefonica = scrapy.Field()
    gas_natural = scrapy.Field()
    generador_electrico = scrapy.Field()
    con_energia_solar = scrapy.Field()
    con_conexion_para_lavarropas = scrapy.Field()
    agua_corriente = scrapy.Field()
    cisterna = scrapy.Field()
    caldera = scrapy.Field()
    chimenea = scrapy.Field()
    gimnasio = scrapy.Field()
    jacuzzi = scrapy.Field()
    estacionamiento_de_visitas = scrapy.Field()
    area_de_cine = scrapy.Field()
    area_de_juegos_infantiles = scrapy.Field()
    con_area_verde = scrapy.Field()
    ascensor = scrapy.Field()
    cancha_de_basquetbol = scrapy.Field()
    con_cancha_de_futbol = scrapy.Field()
    cancha_de_paddle = scrapy.Field()
    cancha_de_tenis = scrapy.Field()
    con_cancha_polideportiva = scrapy.Field()
    salon_de_fiestas = scrapy.Field()
    sauna = scrapy.Field()
    refrigerador = scrapy.Field()
    amoblado = scrapy.Field()
    imagenes = scrapy.Field()
    descripcion = scrapy.Field()
    tipo = scrapy.Field()
    propiedad = scrapy.Field()