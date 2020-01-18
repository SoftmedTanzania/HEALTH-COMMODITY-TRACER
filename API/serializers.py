from django.contrib.auth.models import User
from MasterDataManagement import models as master_data_models
from UserManagement import models as user_management_models
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = user_management_models.Profile
        fields = ('user','birth_date', 'location','reg_id')


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'profile')


class TokenSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = user_management_models.TokenModel
        fields = ('key', 'user')  # there I add the `user` field ( this is my need data ).


class HealthCommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data_models.HealthCommodity
        fields = ('id', 'health_commodity_name', 'description', 'health_commodity_category', 'unit','posting_frequency','has_clients',
                  'track_number_of_patients', 'track_wastage', 'track_quantity_expired', 'is_active', 'elims_product_id')


class HealthCommodityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data_models.HealthCommoditiesCategory
        fields = ('id', 'health_commodity_category_name', 'description', 'is_active')


class HealthCommodityBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data_models.HealthCommodityBalance
        fields = ('id', 'location', 'health_commodity',
                  'quantity_available', 'quantity_consumed', 'user_created','is_active')


class PostingFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data_models.PostingFrequency
        fields = ('id','frequency_description', 'number_of_days', 'is_active')


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data_models.Unit
        fields = ('id', 'abbreviation', 'unit_description', 'is_active')


class HealthCommodityTransactionSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='posting_schedule.health_commodity_balance.health_commodity_id')

    class Meta:
        model = master_data_models.HealthCommodityTransactions
        fields = ('id','posting_schedule', 'product_id', 'trans_date_time', 'quantity_available','quantity_consumed',
                  'has_patients','number_of_clients','quantity_wasted', 'quantity_expired', 'stock_out_days',
                  'user_created', 'is_active')


class PostingScheduleSerializer(serializers.ModelSerializer):
    health_commodity = serializers.CharField(source='health_commodity_balance.health_commodity_id')
    location = serializers.CharField(source='health_commodity_balance.location_id')

    class Meta:
        model = master_data_models.PostingSchedule
        fields = ('id','health_commodity_balance', 'health_commodity','location', 'scheduled_date', 'status')


class FacilityTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.FacilityType
        fields = ('id', 'facility_type_description')


class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.Location
        fields = ('id', 'location_name', 'location_type', 'facility_type', 'parent', 'is_active', 'elims_facility_id')


class MessageRecipientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = master_data_models.MessageRecipient
        fields = ('id','recipient', 'message_id', 'is_read','is_trashed', 'location','deleted_from_mail_box')


class MessagesSerializer(serializers.ModelSerializer):
    message_recipients = MessageRecipientsSerializer(many=True, read_only=True)

    class Meta:
        model = master_data_models.Message
        fields = ('id','date_time_created','message_date_time', 'subject', 'message_body', 'parent_message_id',
                  'trashed_by_creator', 'creator', 'message_recipients')

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ReceivedMessageSerializer(serializers.Serializer):
    message_date_time = serializers.IntegerField()
    creator = serializers.IntegerField()
    message_body = serializers.CharField()
    message_recipients = MessageRecipientsSerializer(many=True)
    parent_message_id = serializers.IntegerField()
    subject = serializers.CharField()


class UpdateElimsConsumptionSerializer(serializers.Serializer):
    elims_facility_id = serializers.CharField(max_length=100)
    elims_product_id = serializers.CharField(max_length=100)
    elims_average_monthly_consumption = serializers.IntegerField()



