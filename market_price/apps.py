from django.apps import AppConfig


class MarketPriceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market_price'
    
    def ready(self):
        from market_price.tasks import fetch_and_store_mandi_prices
        # fetch_and_store_mandi_prices()