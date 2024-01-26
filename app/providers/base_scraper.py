import logging

class BaseScraper:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
        
    def upsert_plan(self, plan_id, provider, product, price, promotion_id=None):
        # Upsert the plan into the database
        self.client.table('plan').upsert({
            'id': str(plan_id),
            'provider': str(provider),
            'product': str(product),
            'price': float(price),
            'promotion': int(promotion_id) if promotion_id else None
        }).execute()
        
    def upsert_promotion(self, price, length):
        # Check if the promotion already exists in the database
        existing_promotion = self.client.table('promotion').select('*').eq('price', price).eq('length', length).execute()
        
        # If it does, get the promotion ID
        if existing_promotion.data:
            promotion_id = existing_promotion.data[0]['id']
        else:
            # Upsert the promotion into the database
            promotion = self.client.table('promotion').upsert({
                'price': float(price), 
                'length': int(length)
            }).execute()
        
            # Get the promotion ID
            promotion_id = promotion.data[0]['id']
            
        return promotion_id