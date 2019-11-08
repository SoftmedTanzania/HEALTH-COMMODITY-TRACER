from django.db import models
from django.contrib.auth.models import User


from mptt.models import MPTTModel, TreeForeignKey


class FacilityType(models.Model):
    def __str__(self):
        return '%s' % self.facility_type_description

    facility_type_description = models.CharField(max_length=150)

    class Meta:
        db_table = "HCT_FacilityTypes"


class Location(MPTTModel):
    COUNTRY = 'CTRY'
    REGION = 'RGN'
    DISTRICT = 'DST'
    FACILITY = 'FCT'

    LOCATION_TYPES = (
        (COUNTRY, 'country'),
        (REGION, 'region'),
        (DISTRICT, 'district'),
        (FACILITY, 'facility'),
    )

    elims_facility_id= models.CharField(max_length=200, null=True, blank=True)
    location_type = models.CharField(max_length=25, choices=LOCATION_TYPES)
    location_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, null=True, blank=True)
    facility_type = models.ForeignKey(FacilityType, on_delete=models.SET_NULL, null=True, blank=True)
    coordinates = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', null=True, blank=True , related_name='children', on_delete=models.SET_NULL)

    def __str__(self):
        return "{}".format(self.location_name)

    def __repr__(self):
        return self.__str__()

    class MPTTMeta:
        db_table = "HCT_Locations"
        order_insertion_by = ['location_name']


class PostingFrequency(models.Model):
    def __str__(self):
        return '%s' % self.frequency_description

    frequency_description = models.CharField(max_length=150)
    number_of_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "HCT_PostingFrequencies"


class Unit(models.Model):
    def __str__(self):
        return "%s" % self.abbreviation

    abbreviation = models.CharField(max_length=30, blank=False)
    unit_description = models.CharField(max_length=150, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "HCT_Units"


class HealthCommoditiesCategory(models.Model):
    def __str__(self):
        return '%s' % self.health_commodity_category_name

    health_commodity_category_name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'HCT_HealthCommoditiesCategories'


class HealthCommodity(models.Model):
    def __str__(self):
        return '%s' % self.health_commodity_name

    health_commodity_name = models.CharField(max_length=150)
    elims_product_id = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    health_commodity_category = models.ForeignKey(HealthCommoditiesCategory, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True)
    posting_frequency = models.ForeignKey(PostingFrequency, on_delete=models.SET_NULL, null=True)
    track_number_of_patients = models.BooleanField(default=False)
    track_wastage = models.BooleanField(default=False)
    track_quantity_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'HCT_HealthCommodities'


class HealthCommodityBalance(models.Model):
    def __str__(self):
        return '%s' % self.health_commodity

    def months_of_stock(self):
        return round(self.quantity_available / self.quantity_consumed, 2)

    health_commodity = models.ForeignKey(HealthCommodity, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_available = models.IntegerField(null=True, blank=True)
    quantity_consumed = models.IntegerField(null=True, blank=True, default=0)
    quantity_wasted = models.IntegerField(null=True, blank=True)
    quantity_expired = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    has_clients = models.BooleanField(null=True, blank=True)
    number_of_clients = models.IntegerField(blank=True, null=True)
    stock_out_days = models.IntegerField(blank=True, null=True)
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "HCT_HealthCommodityBalance"


class PostingSchedule(models.Model):

    def __str__(self):
        return '%s' %self.health_commodity_balance

    def health_commodity(self):
        return self.health_commodity_balance.health_commodity

    def health_facility(self):
        return self.health_commodity_balance.location

    health_commodity_balance = models.ForeignKey(HealthCommodityBalance, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=100, default="pending")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'HCT_PostingSchedule'


class HealthCommodityTransactions(models.Model):
    def __str__(self):
        return '%s' % self.posting_schedule

    date_time_created = models.DateTimeField(auto_now=True)
    trans_date_time = models.BigIntegerField()
    posting_schedule = models.ForeignKey(PostingSchedule, on_delete=models.CASCADE)
    quantity_available = models.IntegerField()
    quantity_consumed = models.IntegerField()
    has_patients = models.BooleanField()
    stock_out_days = models.IntegerField(blank=True, null=True)
    quantity_wasted = models.IntegerField(null=True, blank=True)
    quantity_expired = models.IntegerField(null=True, blank=True)
    number_of_clients = models.IntegerField(blank=True, null=True)
    user_created = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "HCT_HealthCommodityTransactions"


class Message(models.Model):
    def __str__(self):
        return '%d' %self.id

    date_time_created = models.DateTimeField(auto_now=True)
    message_date_time = models.BigIntegerField()
    subject = models.CharField(max_length=150, null=True, blank=True)
    message_body = models.TextField()
    parent_message_id = models.IntegerField(null=True, blank=True, default=0)
    trashed_by_creator = models.BooleanField(default=False)
    deleted_from_mail_box = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "HCT_Messages"


class MessageRecipient(models.Model):
    def __str__(self):
        return '%d' %self.id

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.ForeignKey(Message,related_name='message_recipients', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_trashed = models.BooleanField(default=False)
    deleted_from_mail_box = models.BooleanField(default=False)

    class Meta:
        db_table = "HCT_MessageRecipients"


