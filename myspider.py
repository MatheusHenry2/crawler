import scrapy
import json
import marcas


def write_results_file(marcas):
    marcas_ordenadas = sorted(marcas, key=lambda d: d['name'])
    jsonstring = json.dumps(marcas_ordenadas)
    jsonfile = open('marcas.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


def write_results_file_links(links_marcas):
    print('write result files')
    jsonstring = json.dumps(links_marcas)
    jsonfile = open('links.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


def urls_brands():
    base_url = 'https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter='
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVXWYZ'
    urls = list()
    for l in alfabeto:
        urls.append(base_url + l)
    return urls


def change_urls(self, dados):
    print('change urls aqui')
    total_url = list()
    base_url2 = 'https://www.rankingthebrands.com/'
    for link in dados:
        total_url.append(base_url2 + link)
    write_results_file_links(total_url)


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = urls_brands()
    print(start_urls)
    marcas = list()
    links_descriptions_base = list()
    links_descriptions_base_Full = list()

    def parse(self, response):
        for name in response.css('.brandLine'):
            print('resposta', response.css)
            brand = name.css('::text').get()
            link = name.xpath('.//*[@class="list"]/@href').get()
            self.links_descriptions_base.append(link)
            self.marcas.append({'name': brand, 'urls:': link})
            yield {'name': brand, 'urls': link}

    def close(self, reason):
        self.start_urls.clear()
        change_urls(self, self.links_descriptions_base)
        write_results_file(self.marcas)
