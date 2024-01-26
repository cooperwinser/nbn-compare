import requests
from .base_scraper import BaseScraper

class SuperloopScraper(BaseScraper):
    def get_plans(self):
        # Get the plans
        try:
            url = "https://webservices.api.exetel.com.au/v1/nbn-fibre-plans?fibreType=NbnCo&nbnServiceClass=1&nbnRegion=metro&maxSpeed=1000&flipPlans=0&brand=superloop"
                
            response = requests.get(url)
                
            # Check for 200 response
            if response.status_code != 200:
                self.logger.error(f"Superloop returned a non-200 response: {response.text}")
                return
            
            # Convert the response to JSON
            plans = response.json()
            
            # Loop through the plans and extract the required details
            for plan in plans["plans"]:
                plan_name = plan["planFullSpeed"][4:]
                plan_price = plan["totalMinCost"]
                plan_promo_price = plan["special"]["planPrice"]
                plan_promo_price = "{:.2f}".format(plan_promo_price)
                plan_promo_length = plan["special"]["duration"][:1]
                
                # Check if there is a promotion, and upsert it if there is
                promotion_id = self.upsert_promotion(plan_promo_price, plan_promo_length)
                
                # Upsert the plan into the database
                self.upsert_plan(
                    plan_id = 'superloop_' + plan_name,
                    provider = 'superloop',
                    product = plan_name,
                    price = plan_price,
                    promotion_id = promotion_id if promotion_id else None
                )
                
        # Log any errors
        except Exception as e:
            self.logger.error(f"Failed to get Superloop plans: {e}")
            self.logger.exception(e)