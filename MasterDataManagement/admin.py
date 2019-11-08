from django.contrib import admin
from .models import HealthCommodity, HealthCommoditiesCategory,Unit,\
    FacilityType, HealthCommodityBalance, Location

# Register your models here.


class HealthCommodityAdmin(admin.ModelAdmin):
    list_display = ('health_commodity_name', 'description', 'health_commodity_category', 'unit')
    search_fields = ['health_commodity_name']


class HealthCommoditiesCategoryAdmin(admin.ModelAdmin):
    list_display = ('health_commodity_category_name','description')
    search_fields = ['health_commodity_category_name']


class HealthCommodityFacilityMapping(admin.ModelAdmin):
    list_display = ('health_commodity','location', 'quantity_available')


class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = ('facility_type_description',)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'unit_description',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_type', 'parent')
    search_fields = ['location_name']


admin.site.register(HealthCommodity, HealthCommodityAdmin)
admin.site.register(HealthCommoditiesCategory, HealthCommoditiesCategoryAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(HealthCommodityBalance, HealthCommodityFacilityMapping)
admin.site.register(FacilityType, FacilityTypeAdmin)
admin.site.register(Location, LocationAdmin)

