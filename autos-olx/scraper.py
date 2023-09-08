from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import numpy as np


class Vehiculo(Item):
    marca_vehiculo = Field()
    precio_vehiculo = Field()

class CarroYaCrawler(CrawlSpider):
    
    name = "carroya"

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
      #'CLOSESPIDER_PAGECOUNT': 2 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    download_delay = 1 # tiempo de espera en segundos entre request

    # lista de dominios a los cuales mi spider tiene permitido dirigirse. Si un dominio
    # de una URL no se encuentra en esta lista, mi spider no ira a esta url.
    allowed_domains = [
        "carroya.com"
    ]
    start_urls = [
        "https://www.carroya.com/automoviles-y-camionetas/cali"
    ]
    rules = (
        # paginacion
        Rule(
            LinkExtractor(
                allow=r"/automoviles-y-camionetas/cali?page="
            ), follow=True
        ),
        # detalle de los productos
        Rule(
            LinkExtractor(
                allow=r"/detalle/usado/"
            ), 
            follow=True,
            callback="parse_items"
        )
    )

    def get_unique_value(self, list_text):

        list_text = np.unique(list_text)
        text = "".join(list_text)
        return text


    def parse_items(self, response):
        print("++++++++++++++++", response)
        item = ItemLoader(Vehiculo(), response)
        item.add_xpath("marca_vehiculo", "//h1[@class='title text']/text()", MapCompose(self.get_unique_value))
        item.add_xpath("precio_vehiculo", "//h1[@id='priceInfo']/text()", MapCompose(self.get_unique_value))

        yield item.load_item()
