import requests
from .base_scraper import BaseScraper

class AussieBroadbandScraper(BaseScraper):
    def get_plans(self):
        # Get the plans
        try:
            loc_id = "LOC000181351484"
            url = f"https://wrapper.aussiebroadband.com.au/api/signup/service-qualification/{loc_id}?queue=residential"
            
            response = requests.get(url)
            
            # Check for 200 response
            if response.status_code != 200:
                self.logger.error(f"Aussie Broadband returned a non-200 response: {response.text}")
                return
            
            # Convert the response to JSON
            plans = response.json()
            
            # Loop through the plans and extract the required details
            for plan in plans["broadbandPlans"][:7]:
                plan_name = str(plan["downloadSpeed"]) + "/" + str(plan["uploadSpeed"])
                plan_price = "{:.2f}".format(plan["monthlyCost"])
                    
                # Upsert the plan into the database
                self.upsert_plan(
                    plan_id = 'aussiebroadband_' + plan_name,
                    provider = 'aussiebroadband',
                    product = plan_name,
                    price = plan_price,
                    promotion_id = None
                )
                
        # Log any errors
        except Exception as e:
            self.logger.error(f"Failed to get Aussie Broadband plans: {e}")
            self.logger.exception(e)