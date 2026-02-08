import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta

class ShopManager:
    def __init__(self, refresh_at: datetime, last_refresh: datetime, refresh_interval_hours: int):
        self.refresh_at = refresh_at
        self.last_refresh = last_refresh
        self.refresh_interval_hours = refresh_interval_hours

    def update_shop_refresh(self):
        now = datetime.utcnow()
        interval_hours = timedelta(hours=self.refresh_interval_hours)
        
        if not now >= self.refresh_at:
            return False

        time_elapsed = now - self.last_refresh
        total_refresh_intervals = (time_elapsed // interval_hours) * interval_hours

        update_last_refresh = self.last_refresh + total_refresh_intervals
        update_next_refresh = update_last_refresh + interval_hours

        self.last_refresh = update_last_refresh
        self.refresh_at = update_next_refresh

        return True

    def get_data(self) -> dict:
        data_dict = {
            "refresh_at": self.refresh_at,
            "last_refresh": self.last_refresh,
            "refresh_interval_hours": self.refresh_interval_hours
        }
        return data_dict