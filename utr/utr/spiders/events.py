import scrapy
import json
from datetime import datetime,timedelta
from scrapy.mail import MailSender
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class UtrTournamentsSpiderSpider(scrapy.Spider):
    name = 'utr_tournaments_spider'
    allowed_domains = []
    start_urls = ['https://www.myutr.com/']

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        mailer = MailSender()
        mailer.send(to=["another@example.com"], subject="Scraping", body="The data has been scraped sucessfully", cc=["another@example.com"])
        
    def parse(self, response):
        today = datetime.today()
        start_time = today.strftime("%m/%d/%Y")
        after_90_days = (today+timedelta(days=90)).strftime("%m/%d/%Y")

        start_time = "&range=eventSchedule.eventStartUtc>="+start_time
        end_time ="&range=eventSchedule.eventEndUtc<="+after_90_days 
        url = "https://www.myutr.com/api/v2/search/events?top=1000&skip=0"+start_time+end_time
        yield scrapy.Request(url, callback=self.parse_listing)

    def parse_listing(self, response):
        json_response = json.loads(response.text)
        events = json_response["hits"]
        for event in events:
            source = event.get("source",{})
            event_id  = source.get('id')
            event_url = 'http://www.myutr.com/api/v1/tms/events/%s?optimized=false/'
            event_url = event_url.replace('%s',str(event_id))
            yield scrapy.Request(event_url, callback=self.parse_details, meta={'event_id': str(event_id)})
            event_url = event_url.replace(str(event_id),'%s')


    def parse_details(self,response):
        data = json.loads(response.text)
        players = data['registeredPlayers']
        for player in players:
            data = {
                'displayname' :  player['displayName'],
                'gender' : player['gender'],
                'isPro': player['isPro'],
                'id' : player['id'],
                'location' : player['location']['display'],
                'myUtrSingles': player['myUtrSingles'],
                'myUtrDoubles': player['myUtrDoubles'],
                'myUtrStatusSingles': player['myUtrStatusSingles'],
                'myUtrStatusDoubles': player['myUtrStatusDoubles'],
                'nationality': player['nationality'],
                'event_id' : response.meta.get('event_id')
            }
            yield data