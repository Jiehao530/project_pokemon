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
        next_update = self.next_shop + self.UPDATE_IN
        self.last_generated = self.next_shop
        self.next_shop = next_update
        return True
        
    def model_shop_status(self) -> ShopStatus:
        return ShopStatus(last_generated=self.last_generated, next_shop=self.next_shop)
    
         