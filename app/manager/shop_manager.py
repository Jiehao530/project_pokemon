import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta
from models.shop_model import ShopStatus

class ShopManager:
    UPDATE_IN = timedelta(days=1)

    def __init__(self, last_generated: datetime, next_shop: datetime):
        self.last_generated = last_generated
        self.next_shop = next_shop
    
    def update_shop_status(self):
        now = datetime.utcnow()
        if not now >= self.next_shop:
            return False
        time_elapsed = now - self.last_generated
        days_elapsed = time_elapsed // self.UPDATE_IN
        days = timedelta(days=days_elapsed)
        
        last_update = self.last_generated + days
        next_update = last_update + self.UPDATE_IN
        
        self.last_generated = last_update
        self.next_shop = next_update
        return True
        
    def model_shop_status(self) -> ShopStatus:
        return ShopStatus(last_generated=self.last_generated, next_shop=self.next_shop)
    
         