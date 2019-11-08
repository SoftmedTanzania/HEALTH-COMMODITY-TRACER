from django.urls import path
from MasterDataManagement import views


urlpatterns = [

    path('health_commodity_categories', views.get_health_commodity_categories_page, name='health_commodity_categories'),
    path('health_commodities', views.get_health_commodities_page, name='health_commodities'),
    path('update_commodity/<int:item_pk>/', views.update_health_commodity, name='update_commodity'),
    path('update_category/<int:item_pk>/', views.update_health_commodity_category, name='update_category'),
    path('update_unit/<int:item_pk>/', views.update_unit, name='update_unit'),
    path('update_location/<int:item_pk>/', views.update_location, name='update_location'),
    path('update_frequency/<int:item_pk>/', views.update_frequency, name='update_frequency'),
    path('health_commodities_balance', views.get_commodity_facility_mappings_page, name='health_commodities_balance'),
    # path('get_unmanaged_commodities_by_facility', views.get_unmanaged_commodities_by_facility, name='get_unmanaged_commodities_by_facility'),
    path('get_unmanaged_commodities_by_facility/<int:item_pk>/', views.get_unmanaged_commodities_by_facility, name='get_unmanaged_commodities_by_facility'),
    path('get_post_consumption_page_by_facility/<int:item_pk>/', views.get_post_consumption_page_by_facility, name='get_post_consumption_page_by_facility'),
    path('locations', views.get_location_page, name='locations'),
    path('update_mapping/<int:item_pk>', views.update_mapping, name='update_mapping'),
    path('units', views.get_units_page, name='units'),
    path('frequencies', views.get_frequency_page, name='frequencies'),
    path('commodity_save', views.save_new_commodity, name='new_commodity_save'),
    path('facility_save', views.save_new_facility, name='new_facility_save'),
    path('category_save', views.save_new_category, name='new_category_save'),
    path('unit_save', views.save_new_unit, name='new_unit_save'),
    path('frequency_save', views.save_new_frequency, name='new_frequency_save'),
    path('post_stock_on_hand', views.get_post_stock_on_hand_page, name='post_stock_on_hand'),
    path('post_consumption', views.get_post_consumption_page, name='post_consumption'),
    path('delete_item', views.delete_item, name='delete_item'),
    path('disable_item', views.disable_item, name='disable_item'),
    path('save_commodity_mappings', views.save_mappings, name='save_mappings'),
    path('save_mappings_by_facility', views.save_mappings_by_facility, name='save_mappings_by_facility'),
    path('save_stock_on_hand', views.save_stock_on_hand, name='save_stock_on_hand'),
    path('save_stock_consumed', views.save_consumption, name='save_stock_consumed'),
    path('import_sheet', views.import_sheet, name='import_sheet'),
    path('export_sheet/<str:atype>/', views.export_sheet, name='export_sheet'),
    path('export_posted_transactions_xls/<slug:date_from>/<slug:date_to>/', views.export_posted_transactions_xls, name='export_posted_transactions_xls'),
    path('upload_sheet/', views.upload, name='upload_sheet'),
    path('filter_scheduled_transactions/', views.filter_scheduled_transactions, name='filter_scheduled_transactions'),


]