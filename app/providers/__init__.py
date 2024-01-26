from .aussiebroadband import AussieBroadbandScraper
from .leaptel import LeaptelScraper
from .superloop import SuperloopScraper
from .spintel import SpintelScraper
from .tenmates import TenMatesScraper
from .onethreehundredeasyisp import OneThreeHundredEasyISP
from .twoittechnology import TwoITTechnology

#TODO: Actually schedule this with cron
def schedule_providers_cron(client):
    aussiebroadband_scraper = AussieBroadbandScraper(client)
    aussiebroadband_scraper.get_plans()
    
    leaptel_scraper = LeaptelScraper(client)
    leaptel_scraper.get_plans()
    
    superloop_scraper = SuperloopScraper(client)
    superloop_scraper.get_plans()
    
    spintel_scraper = SpintelScraper(client)
    spintel_scraper.get_plans()
    
    tenmates_scraper = TenMatesScraper(client)
    tenmates_scraper.get_plans()
    
    onethreehundredeasyisp_scraper = OneThreeHundredEasyISP(client)
    onethreehundredeasyisp_scraper.get_plans()
    
    twoittechnology_scraper = TwoITTechnology(client)
    twoittechnology_scraper.get_plans()