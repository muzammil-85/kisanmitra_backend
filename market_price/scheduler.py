
from apscheduler.schedulers.background import BackgroundScheduler
from market_price.tasks import fetch_and_store_mandi_prices

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_mandi_prices, 'interval', days=1)
    scheduler.start()