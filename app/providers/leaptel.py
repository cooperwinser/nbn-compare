from bs4 import BeautifulSoup
import requests
import re
import json
from .base_scraper import BaseScraper

class LeaptelScraper(BaseScraper):
    def get_plans(self):
        # Get the plans
        try:
            url = 'https://leaptel.com.au/nbn-plans/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
            response = requests.get(url, headers=headers)
            
            # Check for 200 response
            if response.status_code != 200:
                self.logger.error(f"Leaptel returned a non-200 response: {response.status_code}")
                return
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the script tag that contains the plans
            plans = soup.select_one('script:-soup-contains("var contract_length")')
            plans = plans.get_text()

            # Extract the value assigned to the 'contract_length' variable (which is a JSON string)
            # Note: this value contains all the plan details, including the plan name, price, etc
            plans_json = re.search(r'var\s+contract_length\s*=\s*(.*?);', plans)

            # Clean the data
            cleaned_plans_json = plans_json.group(1)
            cleaned_plans_json = json.loads(cleaned_plans_json)

            # Loop through the plans and extract the required details
            for plan in cleaned_plans_json:
                for plan_name, sub_plan in plan.items():
                    for sub_plan_id, details in sub_plan.items():
                        # Extract the plan details
                        plan_name = details["speed"]
                        plan_name = plan_name.replace("Mbps", "")
                        
                        plan_promo_price = details["monthly_cost"]
                        plan_promo_price = "{:.2f}".format(plan_promo_price)
                        
                        plan_promo_amount = details["promo_amount"]
                        
                        plan_promo_length = details["promo_month_count"]
                        
                        plan_price = float(plan_promo_price) + float(plan_promo_amount)
                        plan_price = "{:.2f}".format(plan_price)
                        
                        # Check for upload boost on higher plans as JSON pricing data is incorrect
                        # TODO: Find a better way to do this
                        if "Upload Boost" in details["description"]:
                            if plan_name == "250/100" or plan_name == "1000/400":
                                plan_price = float(plan_price)
                                plan_price += 15
                                plan_price = "{:.2f}".format(plan_price)
                        
                        # Check if there is a promotion, and upsert it if there is
                        promotion_id = self.upsert_promotion(plan_promo_price, plan_promo_length)
                        
                        # Upsert the plan into the database
                        self.upsert_plan(
                            plan_id = 'leaptel_' + plan_name,
                            provider = 'leaptel',
                            product = plan_name,
                            price = plan_price,
                            promotion_id = promotion_id if promotion_id else None
                        )
                        
        # Log any errors
        except Exception as e:
            self.logger.error(f"Failed to get Leaptel plans: {e}")