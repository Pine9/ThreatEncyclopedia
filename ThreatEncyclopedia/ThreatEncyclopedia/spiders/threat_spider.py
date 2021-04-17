import scrapy


class ThreatSpider(scrapy.Spider):
    name = "threat"

    start_urls = [
        'https://www.trendmicro.com/vinfo/us/threat-encyclopedia/malware'
    ]

    def parse(self, response):
        # getting every malware entry on the page
        response_list = response.css("div.ContainerListTitle1 a::attr('href')").getall()
        for entry in response_list:
            url = response.urljoin(entry)
            yield scrapy.Request(url=url, callback=self.parse_entry)
        next_page = response.css("li.pagesnumber a::attr('href')").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_entry(self, response):
        # fields: name, type, prefix, platform, suffix/variant, payload, infection channel, memory resident, file type, file size
        # malware naming conventions: https://docs.trendmicro.com/all/ent/tms/v2.5/en-us/tda_2.5_olh/malware_naming.htm
        title = response.css("h1.lessen_h1::text").get().split('.')
        yield {
            'name' : title[2],
            'type' : title[0],
            'prefix' : title[1],
            'suffix' : title[3],
            'platform': response.css("div.entityHeader p::text").getall()[1],
            'payload' : response.css("div.labelHeader::text").getall()[4],
            'infection channel' : response.css("div.labelHeader::text").getall()[0],
            'memory resident?' : response.css("div.labelHeader::text").getall()[3],
            'file type' : response.css("div.labelHeader::text").getall()[2],
            'file size' : response.css("div.labelHeader::text").getall()[1]
        }
