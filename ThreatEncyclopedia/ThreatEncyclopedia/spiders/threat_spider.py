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
        if self.pagenum < self.pages:
            self.pagenum += 1
            next_page = response.urljoin(f"/vinfo/us/threat-encyclopedia/malware/page/{self.pagenum}")
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_entry(self, response):
        # fields: name, platform, infection channel, payload, memory resident, file type, file size, date of sample, date of pattern release
        # official pattern release refers to when the signature was included in the scan engine as an update/new release
        # malware naming conventions: https://docs.trendmicro.com/all/ent/tms/v2.5/en-us/tda_2.5_olh/malware_naming.htm
        title = response.css("h1.lessen_h1::text").get()
        platform = response.css("div.entityHeader p::text").getall()
        if len(platform) > 1:
            platform = platform[1]
        else:
            platform = platform[0]
        infolabels = response.css("div.labelHeader span::text").getall()
        inforesults = response.css("div.labelHeader::text").getall()

        payload = "Unknown"
        channel = "Unknown"
        resident = "Unknown"
        filetype = "Unknown"
        filesize = "Unknown"
        date = "Unknown"
        patterndate = "Unknown"

        for j in range(len(infolabels)):
            if infolabels[j] == 'Infection Channel: ':
                channel = inforesults[j]
            elif infolabels[j] == 'File Size: ':
                filesize = inforesults[j]
            elif infolabels[j] == 'File Type: ':
                filetype = inforesults[j]
            elif infolabels[j] == 'Memory Resident: ':
                resident = inforesults[j]
            elif infolabels[j] == 'Initial Samples Received Date: ':
                date = inforesults[j]
            elif infolabels[j] == 'Payload: ':
                payload = inforesults[j]
            elif infolabels[j] == 'VSAPI OPR PATTERN Date: ':
                patterndate = inforesults[j]

        yield {
            'name' : title,
            'platform': platform,
            'infection channel': channel,
            'payload' : payload,
            'memory resident?' : resident,
            'file type' : filetype,
            'file size' : filesize,
            'date of sample' : date,
            'date of pattern' : patterndate
        }
