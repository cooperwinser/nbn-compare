from bs4 import BeautifulSoup
import requests
import re
from .base_scraper import BaseScraper

class TwoITTechnology(BaseScraper):
    def get_plans(self):
        # Get the plans
        try:
            url = 'https://www.2ittech.com.au/nbn-services/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
            response = requests.get(url, headers=headers)
                        
            # Check for 200 response
            if response.status_code != 200:
                self.logger.error(f"2it Technology returned a non-200 response: {response.status_code}")
                return
                        
            soup = BeautifulSoup(response.content, 'html.parser')
            
            plans_divs = soup.find_all('div', class_='wp-block-column is-layout-flow wp-block-column-is-layout-flow')
            
            # Extract the plans from the plan divs
            for div in plans_divs:
                plan_name = div.find('strong').text.replace("NBN ", "")
                
                # Change 25/5 to 25/10
                if plan_name == "25/5":
                    plan_name = "25/10"
                
                p_tag = div.find('p')
                br_tags = p_tag.find_all('br')
                if len(br_tags) >= 3:
                    plan_price = br_tags[2].find_next_sibling(text=True).strip().replace("$", "")
                    plan_price = "{:.2f}".format(float(plan_price))
                
                # Upsert the plans into the database
                self.upsert_plan(
                        plan_id = 'twoittechnology_' + plan_name,
                        provider = 'twoittechnology',
                        product = plan_name,
                        price = plan_price,
                        promotion_id = None
                )
                
        # Log any errors
        except Exception as e:
            self.logger.error(f"Failed to get 2it Technology plans: {e}")
            self.logger.exception(e)