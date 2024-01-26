import requests
from .base_scraper import BaseScraper

class SpintelScraper(BaseScraper):
    def get_plans(self):
        # Get the plans
        try:
            url = "https://www.spintel.net.au/api/plans/home-internet-nbn?show=details"
                
            response = requests.get(url)
                
            # Check for 200 response
            if response.status_code != 200:
                self.logger.error(f"Spintel returned a non-200 response: {response.text}")
                return
            
            # Convert the response to JSON
            plans = response.json()["data"][2:6]
            
            # Loop through the plans and extract the required details
            for plan in plans:
                plan_name = plan["speed_data"]["feature"]["title"].replace("Mbps", "")
                plan_price = plan["price"]
                plan_promo_price = plan["plan_price_after_credit"]
                plan_promo_length = plan["promotion_months"]
                
                # Spintel has a weird naming convention for their 25/10 plan
                if plan_name == "20/10 Peak":
                    plan_name = "25/10"
                
                # Check if there is a promotion, and upsert it if there is
                promotion_id = self.upsert_promotion(plan_promo_price, plan_promo_length)
                
                # Upsert the plan into the database
                self.upsert_plan(
                    plan_id = 'spintel_' + plan_name,
                    provider = 'spintel',
                    product = plan_name,
                    price = plan_price,
                    promotion_id = promotion_id if promotion_id else None
                )
                
        # Log any errors
        except Exception as e:
            self.logger.error(f"Failed to get Spintel plans: {e}")
            self.logger.exception(e)