def shop_config_converter(data) -> dict:
    return {
        "id": data["_id"],
        "refresh_at": data["refresh_at"],
        "last_refresh": data["last_refresh"],
        "refresh_interval_hours": data["refresh_interval_hours"]
    }