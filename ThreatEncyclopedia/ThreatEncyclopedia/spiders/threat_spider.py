import scrapy


class ThreatSpider(scrapy.Spider):
    name = "threat"
    pages = 50
    pagenum = 1

    start_urls = [
        'https://www.trendmicro.com/vinfo/us/threat-encyclopedia/malware'
    ]

    def parse(self, response):
        # getting every malware entry on the page
        response_list = response.css("div.ContainerListTitle1 a::attr('href')").getall()
        for entry in response_list:
            url = response.urljoin(entry)
            yield scrapy.Request(url=url, callback=self.parse_entry)
        # The html for navigating through the pages is a bit of a mess.
        # However, I know that there are 50 pages
        if self.pagenum <= self.pages:
            self.pagenum += 1
            next_page = response.urljoin(f"/vinfo/us/threat-encyclopedia/malware/page/{self.pagenum}")
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_entry(self, response):
        # fields: name, type, prefix, platform, suffix/variant, payload, infection channel, memory resident, file type, file size
        # malware naming conventions: https://docs.trendmicro.com/all/ent/tms/v2.5/en-us/tda_2.5_olh/malware_naming.htm
        title = response.css("h1.lessen_h1::text").get()
        platform = response.css("div.entityHeader p::text").getall()
        payload = response.css("div.labelHeader::text").getall()
        resident = response.css("div.labelHeader::text").getall()
        fileinfo = response.css("div.labelHeader::text").getall()[2]

        if (len(platform)) > 1:
            platform = platform[1]
        else:
            platform = "Unknown"

        if len(payload) > 4:
            payload = payload[4]
        else:
            payload = "Unknown"

        if len(resident) > 3:
            resident = resident[3]
        else:
            resident = None

        if len(fileinfo) > 2:
            filetype = fileinfo[2]
        else:
            filetype = "Unknown"

        if len(fileinfo) > 1:
            filesize = fileinfo[1]
        else:
            filesize = 0

        """
            'file type' : filetype,
            'file size' : filesize
        """
        # look into prefix and suffix, which unfortunately is not consistent between samples
        yield {
            'full name' : title,
            'platform': platform,
            'payload' : payload,
            'infection channel' : response.css("div.labelHeader::text").get(),
            'memory resident?' : resident
        }
