import scrapy
from unidecode import unidecode
import datetime
import time
import random
from scraping_houses.items import ScrapingHousesItem

class housespider(scrapy.Spider):
    name = "houses"

    def start_requests(self):
        tipo_publicacion = ['venta']#, 'arriendo']
        propiedades = ['casa']#, 'departamento']
        for tipo in tipo_publicacion:
            for propiedad in propiedades:
                url = f"https://www.portalinmobiliario.com/{tipo}/{propiedad}/propiedades-usadas_FiltersAvailableSidebar?filter=state"
                yield scrapy.Request(
                    url = url,
                    callback=self.urls_region,
                    meta={'tipo': tipo, 'propiedad': propiedad}
                )

    def urls_region(self,response):
        tipo = response.meta['tipo']
        propiedad = response.meta['propiedad']
        url_regiones = response.css("a.ui-search-search-modal-filter.ui-search-link::attr(href)").getall()
        regiones = response.css("span.ui-search-search-modal-filter-name::text").getall()
        # Prueba    
        #url_regiones = ['https://www.portalinmobiliario.com/venta/casa/propiedades-usadas/nuble']
        #regiones = ['Ñuble']
        #url_regiones = ['https://www.portalinmobiliario.com/venta/casa/propiedades-usadas/de-los-rios']
        #regiones = ['Los ríos']
        #url_regiones = ['https://www.portalinmobiliario.com/venta/casa/propiedades-usadas/valparaiso']
        #regiones = ['valparaíso']
        for region, url_region in zip(regiones, url_regiones):
            #url = f"https://www.portalinmobiliario.com/{tipo}/{propiedad}/propiedades-usadas/{unidecode(region)}_FiltersAvailableSidebar?filter=city"
            url = url_region
            yield scrapy.Request(
                url = url,
                callback=self.urls_comunas,
                meta={'tipo': tipo, 'propiedad': propiedad, 'region': region}
            )
    def urls_comunas(self,response):
        tipo = response.meta['tipo']
        propiedad = response.meta['propiedad']
        region = response.meta['region']
        filtros = response.css(".ui-search-filter-dl.shops__filter-items")
        for filtro in filtros:
            tipo_filtro = filtro.css("h3.ui-search-filter-dt-title.shops-custom-primary-font::text").get()
            if tipo_filtro == 'Ciudades':
                url_ = filtro.css("a.ui-search-modal__link.ui-search-modal--default.ui-search-link::attr(href)").get()
                if url_ is not None:
                    yield scrapy.Request(
                        url = url_,
                        callback=self.urls_comunas_filtro,
                        meta={'tipo': tipo, 'propiedad': propiedad, 'region': region}
                    )
                else:
                    comunas = filtro.css("span.ui-search-filter-name.shops-custom-secondary-font::text").getall()
                    url_comunas = filtro.css("a.ui-search-link::attr(href)").getall()
                    for comuna, url_comuna in zip(comunas, url_comunas):
                        url = url_comuna
                        yield scrapy.Request(
                            url = url,
                            callback=self.urls_inmuebles,
                            meta={'tipo': tipo, 'propiedad': propiedad, 'region': region, 'comuna': comuna}
                        )

    def urls_comunas_filtro(self,response):
        tipo = response.meta['tipo']
        propiedad = response.meta['propiedad']
        region = response.meta['region']
        url_comunas = response.css("a.ui-search-search-modal-filter.ui-search-link::attr(href)").getall()
        comunas = response.css("span.ui-search-search-modal-filter-name::text").getall()
        for comuna, url_comuna in zip(comunas, url_comunas):
            url = url_comuna
            yield scrapy.Request(
                url = url,
                callback=self.urls_inmuebles,
                meta={'tipo': tipo, 'propiedad': propiedad, 'region': region, 'comuna': comuna}
            )

    def urls_inmuebles(self, response):
        tipo = response.meta['tipo']
        propiedad = response.meta['propiedad']
        comuna = response.meta["comuna"]
        region = response.meta["region"]

        resultado_ = (
            response.css(
                "span.ui-search-search-result__quantity-results.shops-custom-secondary-font::text"
            )   
            .get()
        )

        if '.' in resultado_:
            resultado_ = resultado_.replace('.', '')

        resultado = [int(x) for x in resultado_.split() if x.isdigit()]

        if resultado[0] > 2000:
            comunas_filtro = response.css(".ui-search-money-picker__li")
            urls_comunas_filtro = comunas_filtro.css("a::attr(href)").getall()
            for url in urls_comunas_filtro:
                yield scrapy.Request(
                    url=url,
                    callback=self.urls_inmuebles,
                    meta={'tipo': tipo, 'propiedad': propiedad, "comuna": comuna, "region": region}
                )
        else:
            lista_inmuebles = response.css("div.ui-search-result__wrapper") 
            for casas in lista_inmuebles:
                url_casa = casas.css("a::attr(href)").get()
                yield scrapy.Request(
                    url=url_casa,
                    callback=self.parse_data,
                    meta={'tipo': tipo, 'propiedad': propiedad, "comuna": comuna, "region": region, 'url':url_casa}
                )
                t1 = random.uniform(0.1,0.5)
                time.sleep(t1)

            t2 = random.randint(5, 10)
            time.sleep(t2)

        first_page = response.css(
            "li.andes-pagination__button.andes-pagination__button--next.shops__pagination-button"
        )
        next_page = first_page.css("a::attr(href)").get()
        if next_page is not None:
            yield response.follow(
                next_page,
                callback=self.urls_inmuebles,
                meta={'tipo': tipo, 'propiedad': propiedad, "comuna": comuna, "region": region},
            )

    def parse_data(self, response, **kwargs):
        item = ScrapingHousesItem()
        
        item['precio'] = response.css(".ui-pdp-price__second-line span::text").get()
        item['barrio'] = response.css(".andes-breadcrumb__item:nth-child(6) .andes-breadcrumb__link::text").get()
        item['comuna'] = response.meta["comuna"]
        item['region'] = response.meta["region"]
        item['tipo'] = response.meta["tipo"]
        item['propiedad'] = response.meta["propiedad"]
        item['url'] = response.meta["url"]
        ubicacion_ = response.css(".ui-vip-location__map")
        item['ubicacion'] = ubicacion_.css("img.ui-pdp-image::attr(src)").get()
        item['direccion'] = response.css(
            "p.ui-pdp-color--BLACK.ui-pdp-size--SMALL.ui-pdp-family--REGULAR.ui-pdp-media__title::text"
        ).getall()[-1]
        item['publicacion'] = response.css(
            ".ui-pdp-color--GRAY.ui-pdp-size--XSMALL.ui-pdp-family--REGULAR.ui-pdp-seller-validated__title::text"
        ).get()   
        if item['publicacion'] == "Corredora con ":
            item['publicacion'] = response.css(
                ".ui-pdp-color--GRAY.ui-pdp-size--XSMALL.ui-pdp-family--REGULAR.ui-pdp-header__bottom-subtitle::text"
            ).get()
        
        item['date'] = datetime.datetime.now()

        rows = response.css(".andes-table__row")
        for variable in rows:
            variable_name = variable.css(".andes-table__header__container::text").get()
            if variable_name is not None:
                variable_name = unidecode(variable_name.lower().replace(" ", "_").replace("-", "_"))
                item[variable_name] = variable.css(
                    ".andes-table__column--value::text"
                ).get()

        url_imagenes = []
        imagenes = response.css("span.ui-pdp-gallery__wrapper")
        for imagen in imagenes:
            url = imagen.css("img.ui-pdp-image::attr(data-zoom)").get()
            url_imagenes.append(url)
        item['imagenes'] = url_imagenes
        item['descripcion'] = response.css("p.ui-pdp-description__content::text").getall()

        yield item