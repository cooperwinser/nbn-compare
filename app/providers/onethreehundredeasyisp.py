from bs4 import BeautifulSoup
import requests
import re
from .base_scraper import BaseScraper

class OneThreeHundredEasyISP(BaseScraper):
    def get_plans(self):
        # Get the plans
        try:
            url = 'https://www.1300easyisp.com.au/services/nbn.html'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
            response = requests.get(url, headers=headers)
                    
            # Check for 200 response
            if response.status_code != 200:
                self.logger.error(f"1300EasyISP returned a non-200 response: {response.status_code}")
                return
                    
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the script tag containing the plans
            script_tag = soup.select_one('script:-soup-contains("function setPrice(planSize)")')
            plans_raw = script_tag.text
            
            # Extract the relevant plan names and prices from the script tag
            price_regex = re.compile(r'if\s*\(speed == "(12Mbps|25Mbps|50Mbps|100Mbps)" && planSize == \'XL\'\)\s*price\s*=\s*(\d+);')
            plans = price_regex.findall(plans_raw)
            
            for plan in plans:
                # Get the plan name
                plan_name = plan[0].replace("Mbps", "/")
                if plan_name == "12/":
                    plan_name = "12/1"
                elif plan_name == "25/":
                    plan_name = "25/10"
                elif plan_name == "50/":
                    plan_name = "50/20"
                elif plan_name == "100/":
                    plan_name = "100/40"
                
                # Get the plan price
                plan_price = plan[1]
                plan_price = "{:.2f}".format(float(plan_price))
                
                # Upsert the plans into the database
                self.upsert_plan(
                        plan_id = 'onethreehundredeasyisp_' + plan_name,
                        provider = 'onethreehundredeasyisp',
                        product = plan_name,
                        price = plan_price,
                        promotion_id = None
                )
        
        # Log any errors
        except Exception as e:
            self.logger.error(f"Failed to get 1300EasyISP plans: {e}")
            self.logger.exception(e)
                