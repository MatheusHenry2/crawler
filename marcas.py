import scrapy
import json


def readJson():
    with open("links.json", encoding='utf-8') as meu_json:
        dados = json.load(meu_json)
    print('dados', dados)
    return dados


def writeFile(organization):
    arquivo = open('organization_data.txt', 'w')
    arquivo.write(organization)
    arquivo.close()


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = readJson()
    total_repeticoes = 16838
    organization = list()

    def parse(self, response):
        for title in response.css('#ctl00_mainContent_LBLGBIN'):
            name = response.css('#ctl00_mainContent_LBBrandName::text').get()
            gbin = title.css('::text').get()
            id = response.css('#ctl00_mainContent_LBRTBScore::text').get()
            link = response.css(
                '#ctl00_mainContent_LBBrandWebsite>a::text').get()
            country = response.css(
                '#ctl00_mainContent_LBCountryOfOrigin::text').get()
            industry = response.css(
                '#ctl00_mainContent_LBBrandIndustry>span>a::text').get()
            img_url = response.css(
                '#ctl00_mainContent_LBBrandLogo > img').xpath('@src').get()
            self.total_repeticoes = self.total_repeticoes - 1
            self.organization.append({'NAME': name, 'GBIN': gbin, 'ID': id, 'LINK': link,
                                     'COUNTRY': country, 'INDUSTRY': industry, 'IMAGE': img_url})
            yield {'NAME': name, 'GBIN': gbin, 'ID': id, 'LINK': link, 'COUNTRY': country, 'INDUSTRY': industry, 'IMAGE': img_url}

    def close(self, reason):
            writeFile(self.organization)