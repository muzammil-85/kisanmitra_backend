
from django.urls import path
from .views import ListMarketPriceView, market_prices

urlpatterns = [
    path('market-prices/', market_prices, name='market_prices'),
    path("list-market-price", ListMarketPriceView.as_view(), name="list_market_price")
]
