from django.shortcuts import render


def get_posted_transactions_report(request):
    return render(request, 'Reporting/StockTransactionsReport.html')


def get_stock_trend_report(request):
    return render(request, 'Reporting/MonthsOfStock.html')


def get_stock_balance_report(request):
    return render(request, 'Reporting/StockBalanceReport.html')