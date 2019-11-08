from django.urls import path
from Reporting import views

urlpatterns = [
    path('reporting_posted_transactions',views.get_posted_transactions_report, name='reporting_posted_transactions'),
    path('reporting_stock_trend',views.get_stock_trend_report, name='reporting_stock_trend'),
    path('reporting_stock_balance',views.get_stock_balance_report, name='reporting_stock_balance'),

]