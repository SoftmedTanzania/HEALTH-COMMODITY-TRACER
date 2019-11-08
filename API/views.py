from MasterDataManagement import models as master_data_models
from MasterDataManagement import views as master_data_views
from UserManagement import models as user_management_models
from UserManagement.views import main as user_management_views
from rest_framework import viewsets, status, generics
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from pyfcm import FCMNotification
from django.conf import settings
from .serializers import ProfileSerializer, HealthCommoditySerializer, FacilityTypeSerializer, LocationsSerializer, \
    HealthCommodityTransactionSerializer, \
    UpdatePasswordSerializer, HealthCommodityCategorySerializer, \
    UnitSerializer, PostingScheduleSerializer, HealthCommodityBalanceSerializer, PostingFrequencySerializer, \
    MessagesSerializer, MessageRecipientsSerializer, UserProfileSerializer, ReceivedMessageSerializer,\
    UpdateElimsConsumptionSerializer


# Authentication Views
class ProfileView(viewsets.ModelViewSet):
    queryset = user_management_models.Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)


class UserProfileView(viewsets.ModelViewSet):
    queryset = user_management_models.User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)


class UpdatePasswordView(UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    model = user_management_models.User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateGoogleToken(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    model = user_management_models.Profile
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_id = request.data.get("user")

        if serializer.is_valid:
            queryset = user_management_models.Profile.objects.all()
            instance = queryset.get(user_id=user_id)
            instance.reg_id = request.data.get("reg_id")
            instance.save()

            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateReadMessageRecipientStatus(generics.UpdateAPIView):
    serializer_class = MessageRecipientsSerializer
    model= master_data_models.MessageRecipient
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        message_recipient = request.data.get("id")
        recipient_array = []
        registration_ids= []

        if serializer.is_valid:
            queryset = master_data_models.MessageRecipient.objects.all()
            instance = queryset.get(id=message_recipient)
            instance.is_read = True
            instance.save()

            query_all_recipients = master_data_models.MessageRecipient.objects.filter(message_id =instance.message_id)

            for x in query_all_recipients:
                recipients_object = {"id": message_recipient, "is_read": "true", "message_id": instance.message_id,
                                     "recipient": x.recipient_id}

                recipient_array.append(recipients_object)

            # Send the newly created message and recipients to firebase
            query_message_recipients = master_data_models.MessageRecipient.objects.filter \
                (message_id=instance.message_id).values("recipient_id")

            query_message = master_data_models.Message.objects.filter(id=instance.message_id)
            creator_id = query_message.creator_id

            fcm_tokens = user_management_models.Profile.objects.get(user_id__in=query_message_recipients)
            # creator_fcm_token = user_management_models.Profile.objects.get(user_id=creator_id)

            message_payload = {"type": "NEW_MESSAGE",
                               "data": recipient_array}

            # Send notification to creator
            # creator_fcm_token.send_message(json.dumps(message_payload))

            # Send the newly created message and recipients to firebase
            push_service = FCMNotification(api_key=settings.FCM_APIKEY)

            for x in fcm_tokens:
                registration_ids.append("" + x.reg_id + "")

            result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                                data_message=message_payload)

            print(result)

            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Master-data view
class HealthCommodityView(viewsets.ModelViewSet):
    queryset = master_data_models.HealthCommodity.objects.filter(is_active=True)
    serializer_class = HealthCommoditySerializer
    permission_classes = (IsAuthenticated,)


class HealthCommodityCategoryView(viewsets.ModelViewSet):
    queryset = master_data_models.HealthCommoditiesCategory.objects.filter(is_active=True)
    serializer_class = HealthCommodityCategorySerializer
    permission_classes = (IsAuthenticated,)


class HealthCommodityBalanceView(viewsets.ModelViewSet):
    queryset = master_data_models.HealthCommodityBalance.objects.filter(is_active=True)
    serializer_class = HealthCommodityBalanceSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(request,serializer)
        # headers = self.get_success_headers(serializer.data)

        query_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter(location=request.user.
                                                                                           profile.location)

        query_posting_schedule = master_data_models.PostingSchedule.objects.filter(health_commodity_balance__in=
                                                                                   query_commodity_balance)

        if query_posting_schedule is not None:

            serializer = PostingScheduleSerializer(query_posting_schedule, many=True)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, request, serializer):

        for x in range(0, len(serializer.data)):
            instance = master_data_models.HealthCommodityBalance()

            commodity_id = serializer.data[x]["health_commodity"]
            location_id = serializer.data[x]["location"]

            query_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter(health_commodity_id=
                                                                                               commodity_id, location_id=location_id, is_active=True)

            if query_commodity_balance.count() == 0:
                instance.health_commodity_id = commodity_id
                instance.location_id = location_id
                instance.quantity_available = serializer.data[x]["quantity_available"]
                instance.quantity_consumed = serializer.data[x]["quantity_consumed"]
                instance.user_created_id = serializer.data[x]["user_created"]

                instance.save()

                master_data_views.create_posting_scheduled_for_mapping_created(instance.id)
            elif query_commodity_balance.count() > 0:
                for y in query_commodity_balance:
                    y.quantity_available = serializer.data[x]["quantity_available"]
                    y.quantity_consumed = serializer.data[x]["quantity_consumed"]
                    y.user_created_id = serializer.data[x]["user_created"]
                    y.save()
            else:
                pass

    def list(self, request):
        facility_list = user_management_views.get_facilities_by_user(request).values('id')

        queryset = master_data_models.HealthCommodityBalance.objects.filter(location__in=facility_list, is_active=True)
        serializer = HealthCommodityBalanceSerializer(queryset, many=True)
        return Response(serializer.data)


class PostingFrequencyView(viewsets.ModelViewSet):
    queryset = master_data_models.PostingFrequency.objects.filter(is_active=True)
    serializer_class = PostingFrequencySerializer
    permission_classes = (IsAuthenticated,)


class UnitView(viewsets.ModelViewSet):
    queryset = master_data_models.Unit.objects.filter(is_active=True)
    serializer_class = UnitSerializer
    permission_classes = (IsAuthenticated,)


class FacilityTypeView(viewsets.ModelViewSet):
    queryset = master_data_models.FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer
    permission_classes = (IsAuthenticated,)


class LocationsView(viewsets.ModelViewSet):
    queryset = master_data_models.Location.objects.all()
    serializer_class = LocationsSerializer
    permission_classes = (IsAuthenticated,)


# Flow management views
class HealthCommodityTransactionView(viewsets.ModelViewSet):
    queryset = master_data_models.HealthCommodityTransactions.objects.filter(is_active=True)
    serializer_class = HealthCommodityTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(request,serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, request, serializer):

        for x in range(0, len(serializer.data)):

            instance = master_data_models.HealthCommodityTransactions()
            instance.trans_date_time = serializer.data[x]["trans_date_time"]
            instance.quantity_available = serializer.data[x]["quantity_available"]
            instance.has_patients = serializer.data[x]["has_patients"]
            instance.stock_out_days = serializer.data[x]["stock_out_days"]
            instance.quantity_wasted = serializer.data[x]["quantity_wasted"]
            instance.quantity_consumed = serializer.data[x]["quantity_consumed"]
            instance.quantity_expired = serializer.data[x]["quantity_expired"]
            instance.number_of_clients = serializer.data[x]["number_of_clients"]
            instance.posting_schedule_id = serializer.data[x]["posting_schedule"]
            instance.user_created_id = serializer.data[x]["user_created"]
            instance.quantity_expired = serializer.data[x]["quantity_expired"]

            instance.save()

            query_transactions = master_data_models.HealthCommodityTransactions.objects.get(id=instance.id)

            query_posting_schedule = master_data_models.PostingSchedule.objects.get(id=query_transactions.
                                                                                    posting_schedule_id)
            query_posting_schedule.status = "posted"
            query_posting_schedule.save()

            query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects.get \
                (id=query_transactions.posting_schedule.health_commodity_balance_id)

            query_health_commodity_balance.quantity_available = query_transactions.quantity_available
            query_health_commodity_balance.quantity_wasted = query_transactions.quantity_wasted
            query_health_commodity_balance.quantity_expired = query_transactions.quantity_expired
            query_health_commodity_balance.number_of_clients = query_transactions.number_of_clients
            query_health_commodity_balance.has_clients = query_transactions.has_patients
            query_health_commodity_balance.stock_out_days = query_transactions.stock_out_days
            query_health_commodity_balance.save()

            posting_schedule = serializer.data[x]["posting_schedule"]

            master_data_views.create_schedule_for_commodity_posted(posting_schedule)

    def list(self, request):
        if user_management_views.get_facilities_by_user(request).count() > 0:
            facility_list = user_management_views.get_facilities_by_user(request).values('id')

            queryset = master_data_models.HealthCommodityTransactions.objects.filter \
                (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True)

            serializer = HealthCommodityTransactionSerializer(queryset, many=True)
            return Response(serializer.data)


class PostingScheduleView(viewsets.ModelViewSet):
    queryset = master_data_models.PostingSchedule.objects.filter(is_active=True)
    serializer_class = PostingScheduleSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request):
        if user_management_views.get_facilities_by_user(request).count() > 0:
            facility_list = user_management_views.get_facilities_by_user(request).values('id')

        query_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter \
            (location_id__in=facility_list, is_active=True)
        queryset = master_data_models.PostingSchedule.objects.filter(health_commodity_balance__in=query_commodity_balance)
        serializer = PostingScheduleSerializer(queryset, many=True)
        return Response(serializer.data)


class MessageView(viewsets.ModelViewSet):
    queryset = master_data_models.Message.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(request, serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request):
        query_sent_messages = master_data_models.Message.objects.filter(parent_message_id=0, creator=request.user) \
            .values("id")

        query_message_recipients = master_data_models.MessageRecipient.objects.filter \
            (Q(recipient_id=request.user.id), is_trashed=False).values('message')

        queryset = master_data_models.Message.objects.filter(Q(id__in=query_sent_messages) |
                                                             Q(id__in=query_message_recipients))

        serializer = MessagesSerializer(queryset, many=True)
        return Response(serializer.data)


class MessageRecipientsView(viewsets.ModelViewSet):
    queryset = master_data_models.MessageRecipient.objects.all()
    serializer_class = MessageRecipientsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(request, serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request):
        queryset = master_data_models.MessageRecipient.objects.filter \
            (Q(recipient_id = request.user.id) )

        serializer = MessageRecipientsSerializer(queryset, many=True)
        return Response(serializer.data)


class ReceivedMessageView(generics.CreateAPIView):
    serializer_class = ReceivedMessageSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(self.perform_create(request, serializer))

    def perform_create(self, request, serializer):
        recipients_array = []
        registration_ids = []
        recipients = []
        instance_message = master_data_models.Message()

        message_date_time = serializer.data['message_date_time']
        creator = serializer.data['creator']
        message_body = serializer.data['message_body']
        subject = serializer.data['subject']
        parent_message_id = serializer.data['parent_message_id']

        instance_message.message_date_time = message_date_time
        instance_message.creator_id = creator
        instance_message.message_body = message_body
        instance_message.subject = subject
        instance_message.parent_message_id = parent_message_id
        instance_message.save()

        for val in serializer.data["message_recipients"]:
            is_read = val["is_read"]
            recipient = val["recipient"]

            recipients.append(recipient)

            instance_message_recipients = master_data_models.MessageRecipient()
            instance_message_recipients.is_read = is_read
            instance_message_recipients.message_id = instance_message.id
            instance_message_recipients.recipient_id = recipient
            instance_message_recipients.save()

            recipients_object = {"id": instance_message_recipients.id, "is_read": "false",
                                 "message_id": instance_message.id,
                                 "recipient": recipient}

            recipients_array.append(recipients_object)

        message_object = {"message_date_time": message_date_time, "creator": creator, "id": instance_message.id,
                          "message_body": "" + message_body + "", "message_recipients": recipients_array,
                          "parent_message_id": parent_message_id, "subject": "" + subject + ""}

        message_payload = {"type": "NEW_MESSAGE", "data": message_object}

        # Send the newly created message and recipients to firebase
        fcm_tokens = user_management_models.Profile.objects.filter(user_id__in=recipients)
        push_service = FCMNotification(api_key=settings.FCM_APIKEY)

        for x in fcm_tokens:
            registration_ids.append(""+x.reg_id+"")

        result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                            data_message=message_payload)

        return message_payload


class UpdateParentMessageStatus(generics.UpdateAPIView):
    serializer_class = MessagesSerializer
    model = master_data_models.Message
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        message_id = request.data.get("id")
        is_trashed = request.data.get("trashed_by_creator")

        if serializer.is_valid:
            queryset = master_data_models.Message.objects.all()
            instance = queryset.get(id=message_id)
            instance.trashed_by_creator = is_trashed
            instance.save()

            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMessageRecipientsIsTrashed(generics.UpdateAPIView):
    serializer_class = MessageRecipientsSerializer
    model = master_data_models.MessageRecipient
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        message_recipient = request.data.get("id")
        is_trashed = request.data.get("is_trashed")
        recipient_array = []
        registration_ids = []

        if serializer.is_valid:
            queryset = master_data_models.MessageRecipient.objects.all()
            instance = queryset.get(id=message_recipient)
            instance.is_trashed = is_trashed
            instance.save()

            query_all_recipients = master_data_models.MessageRecipient.objects.filter(
                message_id=instance.message_id)

            for x in query_all_recipients:
                recipients_object = {"id": message_recipient, "is_trashed": is_trashed, "message_id": instance.message_id,
                                     "recipient": x.recipient_id}

                recipient_array.append(recipients_object)

            # Send the newly created message and recipients to firebase
            query_message_recipients = master_data_models.MessageRecipient.objects.filter \
                (message_id=instance.message_id).values("recipient_id")

            query_message = master_data_models.Message.objects.get(id=instance.message_id)
            creator_id = query_message.creator_id

            fcm_tokens = user_management_models.Profile.objects.filter(user_id__in=query_message_recipients)
            # creator_fcm_token = user_management_models.Profile.objects.get(user_id=creator_id)

            message_payload = {"type": "NEW_MESSAGE",
                               "data": recipient_array}

            # Send notification to creator
            # creator_fcm_token.send_message(json.dumps(message_payload))

            # Send the newly created message and recipients to firebase
            push_service = FCMNotification(api_key=settings.FCM_APIKEY)

            for x in fcm_tokens:
                registration_ids.append("" + x.reg_id + "")

            result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                                data_message=message_payload)

            print (result)

            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMessageRecipientsDeletedFromMailbox(generics.UpdateAPIView):
    serializer_class = MessageRecipientsSerializer
    model = master_data_models.MessageRecipient
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        message_recipient = request.data.get("id")
        deleted_from_mail_box = request.data.get("deleted_from_mail_box")
        recipient_array = []
        registration_ids = []

        if serializer.is_valid:
            queryset = master_data_models.MessageRecipient.objects.all()
            instance = queryset.get(id=message_recipient)
            instance.deleted_from_mail_box = deleted_from_mail_box
            instance.save()

            query_all_recipients = master_data_models.MessageRecipient.objects.filter(
                message_id=instance.message_id)

            for x in query_all_recipients:
                recipients_object = {"id": message_recipient, "deleted_from_mail_box": deleted_from_mail_box,
                                     "message_id": instance.message_id,
                                     "recipient": x.recipient_id}

                recipient_array.append(recipients_object)

            # Send the newly created message and recipients to firebase
            query_message_recipients = master_data_models.MessageRecipient.objects.filter \
                (message_id=instance.message_id).values("recipient_id")

            query_message = master_data_models.Message.objects.get(id=instance.message_id)
            creator_id = query_message.creator_id

            fcm_tokens = user_management_models.Profile.objects.filter(user_id__in=query_message_recipients)
            # creator_fcm_token = user_management_models.Profile.objects.get(user_id=creator_id)

            message_payload = {"type": "NEW_MESSAGE",
                               "data": recipient_array}

            # Send notification to creator
            # creator_fcm_token.send_message(json.dumps(message_payload))

            # Send the newly created message and recipients to firebase
            push_service = FCMNotification(api_key=settings.FCM_APIKEY)

            for x in fcm_tokens:
                registration_ids.append("" + x.reg_id + "")

            result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                                data_message=message_payload)

            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateHealthCommodityBalanceConsumptionQuantityFromElmis(generics.UpdateAPIView):
    serializer_class = UpdateElimsConsumptionSerializer
    model = master_data_models.HealthCommodityBalance
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            for x in range(0, len(serializer.data)):
                print(x)
                elims_facility_id = serializer.data[x]["elims_facility_id"]
                elims_product_id = serializer.data[x]["elims_product_id"]
                quantity_consumed = serializer.data[x]["elims_average_monthly_consumption"]

                print(elims_facility_id)

                query_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter \
                    (location__elims_facility_id=""+elims_facility_id+"",
                     health_commodity__elims_product_id=""+elims_product_id+"")

                if query_commodity_balance.count() > 0:
                    for y in query_commodity_balance:
                        y.quantity_consumed = quantity_consumed
                        y.save()
                else:
                    pass

            return Response("Success.", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






