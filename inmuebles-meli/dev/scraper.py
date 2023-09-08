from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class Inmueble(Item):
    titulo = Field()
    precio = Field()
    #descripcion = Field()
    features = Field()
    values = Field()
    coords = Field()
    tipo_inmueble = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = "mercadoLibre"
    
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
      #'CLOSESPIDER_PAGECOUNT': 2 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    download_delay = 1 # tiempo de espera en segundos entre request

    # lista de dominios a los cuales mi spider tiene permitido dirigirse. Si un dominio
    # de una URL no se encuentra en esta lista, mi spider no ira a esta url.
    allowed_domains = [
        "listado.mercadolibre.com.co",
        "apartamento.mercadolibre.com.co",
        "casa.mercadolibre.com.co"
    ]
    start_urls = [
        "https://listado.mercadolibre.com.co/inmuebles/apartamentos/venta/bogota-dc/",
        "https://listado.mercadolibre.com.co/inmuebles/casas/venta/bogota-dc/"
    ]

    # patron, atraves del cual scrapy va ir a los links de los detalles
    rules = (
        
        # paginacion
        # esta regla no tiene callback, dado que en estas paginas principales no queremos
        # traer datos, no queremos parsear ningun dato
        Rule(
            LinkExtractor(
                allow=r"/_Desde_"
            ), follow=True
        ),
        # detalle de los productos
        Rule(
            # link extractor coge todas las urls de la pagina que esta visitando, que cumplan
            # con el patron especificado
            LinkExtractor(
                allow=r"/MCO-"
            ), follow=True, callback="parse_items"
        )
    )
    # nota: scrapy no visita dos paginas con el mismo link, por ejemplo si visito la pagina 2,
    # y luego paso a la pagina 3, scrapy no se devolvera a la pagina 2

    def limpiarTexto(self, texto):
        nuevoTexto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevoTexto
    

    def limpiarCoords(self, texto):
        nuevoTexto = texto.split("center=")[1].split("&")[0].replace("%2C", ",")
        return nuevoTexto


    def parse_items(self, response):
        # dado que la información se va extraer de la pagina del detalle, se le pasa
        # directamente el response al ItemLoader (no hay que pasarle selector)
        item = ItemLoader(Inmueble(), response)
        # mapcompose es para pasarle una funcion que limpie el texto
        item.add_xpath("titulo", "//h1/text()", MapCompose(self.limpiarTexto))
        #item.add_xpath("descripcion", "//p[@class='ui-pdp-description__content']/text()", MapCompose(self.limpiarTexto))
        item.add_xpath("precio", "//span[@class='andes-money-amount__fraction']/text()")
        item.add_xpath("features", "//th[@class='andes-table__header andes-table__header--left ui-vpp-striped-specs__row__column ui-vpp-striped-specs__row__column--id']/text()")
        item.add_xpath("values", "//span[@class='andes-table__column--value']/text()")
        item.add_xpath("coords", "//div[@class='ui-vip-location__map']//img/@src", MapCompose(self.limpiarCoords))
        item.add_xpath("tipo_inmueble", "//span[@class='ui-pdp-subtitle']/text()")
        
        yield item.load_item()
