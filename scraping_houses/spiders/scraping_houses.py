import scrapy
from unidecode import unidecode
import datetime
from scraping_houses.items import ScrapingHousesItem

class housespider(scrapy.Spider):
    name = "houses"

    def start_requests(self):
        comunas = ['Calera-de-tango']
        regiones = ["Metropolitana"]
        for region in regiones:
            for comuna in comunas:
                url_comuna =  f"https://www.portalinmobiliario.com/venta/casa/propiedades-usadas/{unidecode(comuna)}-{region}/_NoIndex_True"
                yield scrapy.Request(
                    url=url_comuna,
                    callback=self.urls_casas,
                    meta={"comuna": comuna, "region": region}
                )

    def urls_casas(self, response):
        comuna = response.meta["comuna"]
        region = response.meta["region"]

        resultado_ = (
            response.css(
                ".ui-search-search-result__quantity-results.shops-custom-secondary-font::text"
            )
            .get()
            .replace(".", "")
        )
        resultado = [int(x) for x in resultado_.split() if x.isdigit()]

        if resultado[0] > 2000:
            comunas_filter = response.css(".ui-search-money-picker__li")
            urls_comuna_filter = comunas_filter.css("a::attr(href)").getall()
            for url in urls_comuna_filter:
                yield scrapy.Request(
                    url=url,
                    callback=self.urls_casas,
                    meta={"comuna": comuna, "region": region}
                )
        
        lista_casas = response.css("div.ui-search-result__wrapper")
        for casas in lista_casas:
            url_casa = casas.css("a::attr(href)").get()
            yield scrapy.Request(
                url=url_casa,
                callback=self.parse_casa_data,
                meta={"comuna": comuna, "region": region}
            )

        first_page = response.css(
            "li.andes-pagination__button.andes-pagination__button--next.shops__pagination-button"
        )
        next_page = first_page.css("a::attr(href)").get()
        if next_page is not None:
            yield response.follow(
                next_page,
                callback=self.urls_casas,
                meta={"comuna": comuna, "region": region},
            )

    def parse_casa_data(self, response, **kwargs):
        item = ScrapingHousesItem()
               
        item['precio'] = response.css(".ui-pdp-price__second-line span::text").get()
        item['comuna'] = response.meta["comuna"]
        item['region'] = response.meta["region"]
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