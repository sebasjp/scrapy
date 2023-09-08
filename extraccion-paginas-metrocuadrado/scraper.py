from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

class Page(Item):
    titulo = Field()
    contenido = Field()
    url = Field()

class MetrocuadradoLinksCrawler(CrawlSpider):
    name = "metrocuadrado_links"
    
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
      #'CLOSESPIDER_PAGECOUNT': 2 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    download_delay = 1 # tiempo de espera en segundos entre request

    # lista de dominios a los cuales mi spider tiene permitido dirigirse. Si un dominio
    # de una URL no se encuentra en esta lista, mi spider no ira a esta url.
    allowed_domains = [
        "metrocuadrado.com"
    ]
    start_urls = [
        "https://metrocuadrado.com/noticias/",
    ]

    # patron, atraves del cual scrapy va ir a los links de los detalles
    rules = (        
        # paginacion
        # esta regla no tiene callback, dado que en estas paginas principales no queremos
        # traer datos, no queremos parsear ningun dato
        Rule(
            LinkExtractor(
                allow=r"/actualidad/"
            ), follow=True, callback="parse_items"
        ),
    )
    # nota: scrapy no visita dos paginas con el mismo link, por ejemplo si visito la pagina 2,
    # y luego paso a la pagina 3, scrapy no se devolvera a la pagina 2

    
    def parse_items(self, response):
        # url = response.url
        # if "tags/" not in url:
        #    yield {'url': url}
        item = ItemLoader(Page(), response)
        item.add_value("url", response.url)
        item.add_xpath("titulo", "//h1[@property='dc:title']/text()")
        item.add_xpath("contenido", "//div[@class='article-text']//text()")

        
