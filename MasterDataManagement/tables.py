import django_tables2 as tables
from .models import HealthCommoditiesCategory, HealthCommodity, Unit, HealthCommodityBalance, PostingFrequency, \
    Location
from django.utils.safestring import mark_safe
from django.utils.html import escape


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-xs"><i class="la la-trash"></i></button> '
                         '<button id="%s" class="btn_update btn btn-success '
                         'btn-xs"><i class="la la-pencil"></i></button> ' % (escape(record.id), escape(record.id)))


class Delete(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn-xs btn-danger'
                         '"><i class="la la-trash"></i></button> ' % (escape(record.id)))


class IsManaged(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe(' <input type="checkbox" class="switch" value="%s" name="is_managed" data-reverse />'
                         % (escape(record.id)))


class StockOnHand(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe(' <input placeholder="Enter Stock On Hand" type="number" '
                         'class="textinput input-sm textInput form-control" name="id_quantity_available" />')


class StockConsumed(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe(' <input placeholder="Enter Stock Consumed" type="number" '
                         'class="textinput input-sm textInput form-control" name="id_quantity_consumed" />')


class RecordId(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe(' <input type="text" '
                         'class="textinput input-sm textInput form-control" value="%s" name="record_id" hidden />'
                         % (escape(record.id)))


class HealthCommodityCategoriesTable(tables.Table):
    Actions = Actions()
    id = tables.Column(verbose_name='ID')
    health_commodity_category_name = tables.Column(verbose_name='Category Name')
    description = tables.Column(verbose_name='Description')

    class Meta:
        model = HealthCommoditiesCategory
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'health_commodity_category_name', 'description')


class HealthCommoditiesTable(tables.Table):
    Actions = Actions()

    health_commodity_category = tables.Column(attrs={
        'td': {
            'class': 'category'
        }
    })

    class Meta:
        model = HealthCommodity
        row_attrs = {
            'data-id': lambda record: record.pk,
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'health_commodity_name','elims_product_id', 'description', 'health_commodity_category', 'unit', 'posting_frequency')


class ManageHealthCommoditiesTable(tables.Table):
    Commodity_Managed_In_Facility = IsManaged()

    health_commodity_category = tables.Column(attrs={
        'td': {
            'class': 'category'

        }
    })

    class Meta:
        model = HealthCommodity
        attrs = {'class': 'table', 'id':'table_manage_commodities'}
        row_attrs = {
            'data-id': lambda record: record.pk,
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'health_commodity_name','health_commodity_category', 'unit')


class UnitsTable(tables.Table):
    Actions = Actions()

    class Meta:
        model = Unit
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'abbreviation', 'unit_description')


class PostingFrequencyTable(tables.Table):
    Actions = Actions()

    class Meta:
        model = PostingFrequency
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'frequency_description', 'number_of_days')


class HealthCommodityBalanceTable(tables.Table):
    Actions = Actions()
    quantity_available = tables.Column(verbose_name='Stock On Hand(SOH)')
    quantity_consumed = tables.Column(verbose_name='Average Monthly Consumption(AMC)')
    quantity_wasted = tables.Column(verbose_name='Quantity Wasted')
    quantity_expired = tables.Column(verbose_name='Quantity Expired')
    location = tables.Column(accessor="location.location_name", verbose_name='Facility Name')
    number_of_clients = tables.Column( verbose_name='Number of Clients')
    # months_of_stock = tables.Column(accessor=)

    class Meta:
        model = HealthCommodityBalance
        row_attrs = {
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id','location', 'health_commodity','months_of_stock','stock_out_days', 'quantity_available',
                  'quantity_consumed','quantity_wasted', 'quantity_expired',
                  'has_clients','number_of_clients')


class PostStockBalanceTable(tables.Table):
    Quantity_Available = StockOnHand()
    unit = tables.Column(accessor='health_commodity.unit.unit_description')
    Action = RecordId()

    class Meta:
        model = HealthCommodityBalance
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'health_commodity', 'unit')


class PostConsumptionTable(tables.Table):
    Average_Monthly_Consumption = StockConsumed()
    location = tables.Column(accessor='location.location_name', verbose_name='Facility Name')
    unit = tables.Column(accessor='health_commodity.unit.unit_description')
    Action = RecordId()

    class Meta:
        model = HealthCommodityBalance
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'health_commodity', 'unit', 'quantity_available','Average_Monthly_Consumption', 'location')


class LocationTable(tables.Table):
    Actions = Actions()
    class Meta:
        model = Location
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id','elims_facility_id', 'location_name','location_type', 'facility_type', 'coordinates')
