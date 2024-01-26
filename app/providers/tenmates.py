from bs4 import BeautifulSoup
import requests
from .base_scraper import BaseScraper

class TenMatesScraper(BaseScraper):
    def get_plans(self):
        # Get the plans
        try:
            url = 'https://10mates.com.au/packages/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
            response = requests.get(url, headers=headers)
                
            # Check for 200 response
            if response.status_code != 200:
                self.logger.error(f"10Mates returned a non-200 response: {response.status_code}")
                return
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            plan_names_cleaned = []
            plan_prices_cleaned = []
            
            # Extract the plan names from the page
            plan_names = [p for p in soup.find_all('span', class_='elementor-icon-list-text') if p.text.startswith("Up to")]
            for plan_name in plan_names[4:]: # 10Mates has "budget" and "premium" plans. We only want the premium plans.
                plan_name = plan_name.text.replace("Up to ", "")
                plan_name = plan_name[:-4]
                plan_names_cleaned.append(plan_name)
            
            # Extract the plan prices from the page
            plan_prices = [div for div in soup.find_all('div', class_='elementor-heading-title elementor-size-default') if div.text.startswith("$")]
            for plan_price in plan_prices[4:]:
                plan_price = plan_price.text.replace("$", "")
                plan_price = "{:.2f}".format(float(plan_price))
                plan_prices_cleaned.append(plan_price)
                
            # Upsert the plans into the database
            for plan_name, plan_price in zip(plan_names_cleaned, plan_prices_cleaned):
                self.upsert_plan(
                    plan_id = 'tenmates_' + plan_name,
                    provider = 'tenmates',
                    product = plan_name,
                    price = plan_price,
                    promotion_id = None
                )
                
        # Log any errors
        except Exception as e:
            self.logger.error(f"Failed to get 10Mates plans: {e}")
            self.logger.exception(e)
            