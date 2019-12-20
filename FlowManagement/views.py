from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .tables import HealthCommodityTransactionTable,ScheduledTransactionTable, MessageInboxTable, MessageSentTable, \
    MessageTrashedTable
from MasterDataManagement import models as master_data_models
from MasterDataManagement import views as master_data_views
from UserManagement.views import main as user_management_views
from UserManagement import models as user_management_models
from .forms import PostCommodityForm, ComposeMessageForm, MessageRecipientsForm
from django_tables2 import RequestConfig
from django.apps import apps

from datetime import datetime
from datetime import timedelta
from django.db.models import Count
from django.db.models import Q
import json

from pyfcm import FCMNotification
from django.conf import settings
import requests
from background_task import background
from dateutil.relativedelta import relativedelta


elmis_username = 'mkassongo'
elmis_password = 'Kingdom6'
elmis_server = 'https://elmis.co.tz/j_spring_security_check'
hct_username = 'admin'
hct_password = 'Tracer123$'
hct_server = 'http://173.255.220.51'
params = {
    'j_username': elmis_username,
    'j_password': elmis_password
}

payload_json_array = []


def get_scheduled_transaction_page(request):
    if user_management_views.get_facilities_by_user(request).count() > 0:
        facility_list = user_management_views.get_facilities_by_user(request).values('id')

        locations = user_management_views.get_parent_child_relationship(request)

        query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects. \
            filter(location__in=facility_list, health_commodity__is_active=True)

        table_scheduled_transactions = ScheduledTransactionTable(master_data_models.PostingSchedule.objects.
                                                                 filter(health_commodity_balance__is_active=True,status="pending", health_commodity_balance__in=
        query_health_commodity_balance).order_by('scheduled_date'))

        RequestConfig(request, paginate={'per_page': 50}).configure(table_scheduled_transactions)

        notifications = get_dashboard_notification_count(request)

        unread_messages = notifications[0]
        scheduled_items = notifications[1]

        return render(request, 'FlowManagement/ScheduledTransactions.html',
                      {'table_scheduled_transactions': table_scheduled_transactions,'unread_messages':unread_messages,
                       'scheduled_items':scheduled_items, 'locations':locations})


def get_repost_schedules_page(request):
    query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter(location=
                                                                                              request.user.
                                                                                              profile.location, health_commodity__is_active=True)

    table_posted_transactions = ScheduledTransactionTable(master_data_models.PostingSchedule.objects.
                                                          filter(health_commodity_balance__is_active=True,status="posted", health_commodity_balance__in=
    query_health_commodity_balance))

    RequestConfig(request, paginate={'per_page': 15}).configure(table_posted_transactions)

    notifications = get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'FlowManagement/RepostSchedule.html',
                  {'table_posted_transactions': table_posted_transactions, 'unread_messages':unread_messages,
                   'scheduled_items':scheduled_items
                   })


def view_health_commodity_transactions(request):
    facility_list = user_management_views.get_facilities_by_user(request).values('id')

    query_transactions = master_data_models.HealthCommodityTransactions.objects.filter(is_active=True,
                                                                                       posting_schedule__health_commodity_balance__location__in=facility_list).order_by('-id')
    table_transactions = HealthCommodityTransactionTable(query_transactions)

    RequestConfig(request, paginate={'per_page': 50}).configure(table_transactions)

    notifications = get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'FlowManagement/ViewTransactions.html', {'table_transactions':
                                                                        table_transactions, 'unread_messages':unread_messages,
                                                                    'scheduled_items':scheduled_items})


def get_facility_by_post(request):

    count_location_transactions = master_data_models.HealthCommodityTransactions.objects \
        .values('posting_schedule__health_commodity_balance__location__location_name',
                'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
        .annotate(count=Count('posting_schedule')) \
        .order_by('posting_schedule__health_commodity_balance__location__location_name')

    notifications = get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'FlowManagement/HeathFacilities.html', {'count_location_transactions':
                                                                       count_location_transactions,
                                                                   'unread_messages':unread_messages,
                                                                   'scheduled_items':scheduled_items})


def get_message_thread_page(request, item_pk):

    query_message = master_data_models.Message.objects.get(id=item_pk)
    message_id = item_pk
    subject = query_message.subject
    message_body = query_message.message_body
    recipients = master_data_models.MessageRecipient.objects.filter(message_id=item_pk).values("recipient")

    recipient_names = User.objects.filter(id__in=recipients)

    query_message_thread = master_data_models.Message.objects.filter(parent_message_id=item_pk)

    # update message status to read
    mark_all_thread_as_read(request, item_pk)

    notifications = get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'FlowManagement/MessageContent.html', {'message_id': message_id,
                                                                  'subject':subject, 'message_body': message_body,
                                                                  'query_message_thread':query_message_thread,
                                                                  'unread_messages':unread_messages,
                                                                  'scheduled_items':scheduled_items,
                                                                  'recipient_names':recipient_names})


def mark_all_thread_as_read(request, item_pk):
    query_messages = master_data_models.Message.objects.filter(parent_message_id=item_pk).values('id')
    query_message_thread_by_recipient = master_data_models.MessageRecipient.objects.filter(message_id__in=query_messages,
                                                                                           recipient_id=request.user.id)
    if query_message_thread_by_recipient.count() > 0:

        for x in query_message_thread_by_recipient:
            x.is_read = True
            x.save()

    query_original_message_recipient = master_data_models.MessageRecipient.objects.filter(message_id=item_pk)

    if query_original_message_recipient.count() > 0:

        for x in query_original_message_recipient:
            x.is_read = True
            x.save()


def get_post_commodity_page(request, item_pk):
    query_schedule = master_data_models.PostingSchedule.objects.get(id=item_pk)

    facility_name = query_schedule.health_commodity_balance.location.location_name

    scheduled_date = query_schedule.scheduled_date

    query_commodity = master_data_models.HealthCommodity.objects.get(id=query_schedule.
                                                                     health_commodity_balance.health_commodity_id)

    # reporting_period = round(30/query_schedule.health_commodity_balance.health_commodity.posting_frequency.number_of_days)

    form_post_commodity = PostCommodityForm(initial={'posting_schedule': item_pk, 'quantity_consumed':query_schedule.
                                            health_commodity_balance.quantity_consumed})

    notifications = get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'FlowManagement/PostCommodity.html',{'form_post_commodity': form_post_commodity,
                                                                'scheduled_date': scheduled_date,
                                                                'query_commodity':query_commodity,
                                                                'unit':query_commodity.unit,
                                                                'facility':facility_name,
                                                                'commodity':query_commodity.health_commodity_name,
                                                                'frequency': query_commodity.posting_frequency.number_of_days,
                                                                'unread_messages':unread_messages,
                                                                'scheduled_items':scheduled_items
                                                                })


def check_for_commodities_to_post(request):
    facility_list = user_management_views.get_facilities_by_user(request).values('id')

    query_managed_commodities = master_data_models.HealthCommodityBalance.objects.filter \
        (location__in=facility_list)

    if query_managed_commodities.count() > 0:
        query_schedule = master_data_models.PostingSchedule.objects.filter \
            (health_commodity_balance__is_active=True,health_commodity_balance__in=query_managed_commodities, scheduled_date__lte=datetime.now(),
             status="pending")

        return query_schedule
    else:
        return None


def get_messaging_page(request):

    form_message = ComposeMessageForm()
    form_recipients = MessageRecipientsForm()

    query_users = user_management_models.User.objects.exclude(id=request.user.id)

    query_trashed_messages = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                is_trashed=True,
                                                                                deleted_from_mail_box=False).values('message')

    table_inbox = inbox_items(request)

    notifications = get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    table_sent = MessageSentTable(master_data_models.Message.objects.filter(creator_id=request.user.id,
                                                                            parent_message_id=0,
                                                                            trashed_by_creator=False))

    table_trash = MessageTrashedTable(master_data_models.Message.objects.filter(Q(id__in=query_trashed_messages) |
                                                                                Q(trashed_by_creator=True) &
                                                                                Q(creator=request.user)))

    RequestConfig(request, paginate={'per_page': 30}).configure(table_inbox)
    RequestConfig(request, paginate={'per_page': 30}).configure(table_sent)
    RequestConfig(request, paginate={'per_page': 30}).configure(table_trash)

    return render(request, 'FlowManagement/Messaging.html', {'form_message':form_message, 'form_recipients':
        form_recipients, 'table_inbox': table_inbox, 'table_sent':table_sent, 'table_trash':table_trash,
                                                             'query_users':query_users, 'unread_messages':unread_messages,
                                                             'scheduled_items':scheduled_items})


def get_dashboard_notification_count(request):
    query_message_recipients = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                  is_trashed=False, is_read=False,
                                                                                  deleted_from_mail_box=False).values(
        'message')
    query_inbox = master_data_models.Message.objects.filter((Q(id__in=query_message_recipients) &
                                                             Q(parent_message_id__gte=0)))

    unread_message_count = query_inbox.count()

    query_post_commodities = check_for_commodities_to_post(request)

    if query_post_commodities is not None:
        scheduled_items = query_post_commodities.count()
    else:
        scheduled_items = 0

    return [unread_message_count, scheduled_items]


def save_posted_transaction(request):
    if request.POST:
        form = PostCommodityForm(request.POST)

        if form.is_valid():
            form.full_clean()
            instance = form.save(commit=False)
            instance.trans_date_time = datetime.now().timestamp()
            instance.user_created = request.user
            instance.save()

            query_transactions = master_data_models.HealthCommodityTransactions.objects.get(id=instance.id)

            query_posting_schedule = master_data_models.PostingSchedule.objects.get(id=query_transactions.
                                                                                    posting_schedule_id)
            query_posting_schedule.status = "posted"
            query_posting_schedule.save()

            # # Update the latest balance
            # query_transactions_order_received = master_data_models.HealthCommodityTransactions.\
            #     objects.filter(posting_schedule__health_commodity_balance__location=request.user.profile.location).order_by("-trans_date_time")
            #
            # if query_transactions.trans_date_time > query_transactions_order_received.trans_date_time:
            query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects.get \
                (id=query_transactions.posting_schedule.health_commodity_balance_id)

            query_health_commodity_balance.quantity_available = query_transactions.quantity_available
            query_health_commodity_balance.quantity_wasted = query_transactions.quantity_wasted
            query_health_commodity_balance.quantity_expired = query_transactions.quantity_expired
            query_health_commodity_balance.has_clients = query_transactions.has_patients
            query_health_commodity_balance.number_of_clients = query_transactions.number_of_clients
            query_health_commodity_balance.stock_out_days = query_transactions.stock_out_days
            query_health_commodity_balance.save()

            master_data_views.create_schedule_for_commodity_posted(instance.posting_schedule_id)

        return redirect(request.META['HTTP_REFERER'])
    else:
        pass


def send_user_a_push_notification(request):
    registration_ids = []

    if request.method == "POST":

        recipients = request.POST["recipients"].split(',')
        form = ComposeMessageForm(request.POST)

        if form.is_valid():
            form.full_clean()
            instance = form.save(commit=False)
            instance.message_date_time = datetime.now().timestamp()
            instance.creator = request.user
            instance.save()

            # Message object elements
            recipients_array = []
            message_time_stamp = int(datetime.now().timestamp()) * 1000
            creator_id = request.user.id
            message_body = form.cleaned_data['message_body']
            subject = form.cleaned_data['subject']
            message_id = instance.id

            for x in range(len(recipients)):
                instance_message_recipients = master_data_models.MessageRecipient()
                instance_message_recipients.message_id = instance.id
                instance_message_recipients.recipient_id = recipients[x]
                instance_message_recipients.save()

                recipients_object = {"id":instance_message_recipients.id, "is_read": "false", "message_id": message_id,
                                     "recipient": recipients[x]}

                recipients_array.append(recipients_object)

            message_object = {"message_date_time": message_time_stamp, "creator": creator_id, "id": message_id,
                              "message_body": "" + message_body + "", "message_recipients": recipients_array,
                              "parent_message_id": 0, "subject": "" + subject + ""}

            message_payload = {"type": "NEW_MESSAGE", "data": message_object}

            # Send the newly created message and recipients to firebase
            fcm_tokens = user_management_models.Profile.objects.filter(user_id__in=recipients)
            push_service = FCMNotification(api_key=settings.FCM_APIKEY)

            for x in fcm_tokens:
                # if x.reg_id is not None:
                #     x.send_message(json.dumps(message_payload))
                registration_ids.append("" + x.reg_id + "")

            result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                                data_message=message_payload)
            print (result)

        return redirect(request.META['HTTP_REFERER'])


def send_thread_message(request):
    if request.method == "POST":
        message_id = request.POST["message_id"]
        message = request.POST["message"]
        registration_ids = []
        recipients_array = []

        message_time_stamp = int(datetime.now().timestamp()) * 1000

        instance = master_data_models.Message()
        instance.message_date_time = datetime.now().timestamp()
        instance.message_body = message
        instance.parent_message_id = message_id
        instance.creator_id = request.user.id
        instance.save()

        query_parent_recipients = master_data_models.MessageRecipient.objects.filter(message_id=message_id)

        for x in query_parent_recipients:
            instance_recipients = master_data_models.MessageRecipient()
            instance_recipients.message_id = instance.id
            instance_recipients.recipient_id = x.recipient_id
            instance_recipients.save()

            recipients_array.append(x.recipient_id)

        # insert the creator as a recipient too
        query_original_message = master_data_models.Message.objects.get(id=message_id, parent_message_id=0)
        instance_recipients = master_data_models.MessageRecipient()

        instance_recipients.message_id = instance.id
        instance_recipients.recipient_id = query_original_message.creator_id
        instance_recipients.save()

        message_object = {"message_date_time": message_time_stamp, "creator": request.user.id, "id": message_id,
                          "message_body": "" + message + "", "message_recipients": recipients_array,
                          "parent_message_id": message_id, "subject": ""}

        message_payload = {"type": "THREAD_MESSAGE", "data": message_object}

        # Send the newly created message and recipients to firebase
        recipients = master_data_models.MessageRecipient.objects.filter(message_id=message_id).values("recipient")
        fcm_tokens = user_management_models.Profile.objects.filter(user_id__in=recipients)
        push_service = FCMNotification(api_key=settings.FCM_APIKEY)

        for x in fcm_tokens:
            registration_ids.append("" + x.reg_id + "")

        result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                            data_message=message_payload)
        print(result)
    return redirect(request.META['HTTP_REFERER'])


def trash_email(request):
    if request.method == "POST":
        item_pk = int(request.POST["item_pk"])
        model_name = (request.POST["model"])
        app_name = (request.POST["app_name"])
        origin = (request.POST["origin"])

        model = apps.get_model(app_name, model_name)

        query = model.objects.filter(message_id=item_pk, recipient=request.user)

        for x in query:
            x.is_trashed = True
            x.save()

        query_message = master_data_models.Message.objects.get(id=item_pk)

        if request.user == query_message.creator:
            query_message.trashed_by_creator = True
            query_message.save()

            if origin == "inbox":
                path = load_inbox(request)

            elif origin == "sent":
                path = load_sent_items(request)

            return path

    return redirect(request.META['HTTP_REFERER'])


def trash_inbox_message(request):
    if request.method == "POST":
        item_pk = int(request.POST["item_pk"])
        model_name = (request.POST["model"])
        app_name = (request.POST["app_name"])
        origin = (request.POST["origin"])

        model = apps.get_model(app_name, model_name)

        query = model.objects.filter(message_id=item_pk, recipient=request.user)

        for x in query:
            x.is_trashed = True
            x.save()

        query_message = master_data_models.Message.objects.get(id=item_pk)

        if request.user == query_message.creator:
            query_message.trashed_by_creator = True
            query_message.save()

    path = load_inbox(request)

    return HttpResponse(path)


def untrash_email(request):
    if request.method == "POST":
        item_pk = int(request.POST["item_pk"])
        model_name = (request.POST["model"])
        app_name = (request.POST["app_name"])

        model = apps.get_model(app_name, model_name)

        query = model.objects.filter(message_id=item_pk, recipient=request.user)

        for x in query:
            x.is_trashed = False
            x.save()

        query_message = master_data_models.Message.objects.get(id=item_pk)

        if request.user == query_message.creator:
            query_message.trashed_by_creator = False
            query_message.save()

    table_trash = trash_items(request)

    return render(request, 'FlowManagement/MessagingComponents.html', {'table':table_trash, "title": "Trashed Items"})


def inbox_items(request):
    query_sent_messages = master_data_models.Message.objects.filter(parent_message_id__gt=0) \
        .values("parent_message_id")

    query_message_recipients = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                  is_trashed=False).values(
        'message')

    table_inbox = MessageInboxTable(master_data_models.Message.objects.filter((Q(id__in=query_sent_messages) &
                                                                               Q(creator=request.user) &
                                                                               Q(trashed_by_creator=False) &
                                                                               Q(parent_message_id=0)) | (
                                                                                  Q(
                                                                                      id__in=query_message_recipients) &
                                                                                  Q(parent_message_id=0))))

    return table_inbox


def sent_items(request):
    table_sent = MessageSentTable(master_data_models.Message.objects.filter(creator_id=request.user.id,
                                                                            parent_message_id=0,
                                                                            trashed_by_creator=False))

    return table_sent


def trash_items(request):
    query_trashed_messages = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                is_trashed=True, deleted_from_mail_box=False
                                                                                ).values('message')
    table_trash = MessageTrashedTable(
        master_data_models.Message.objects.filter(Q(id__in=query_trashed_messages) |
                                                  Q(trashed_by_creator=True) & Q(deleted_from_mail_box=False) &
                                                  Q(creator=request.user)))

    return table_trash


def load_inbox(request):
    if request.method == "POST":
        query_sent_messages = master_data_models.Message.objects.filter(parent_message_id__gt=0) \
            .values("parent_message_id")

        query_message_recipients = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                      is_trashed=False).values(
            'message')

        query_inbox = master_data_models.Message.objects.filter((Q(id__in=query_sent_messages) &
                                                                 Q(creator=request.user) &
                                                                 Q(trashed_by_creator=False) &
                                                                 Q(parent_message_id=0)) | (
                                                                    Q(id__in=query_message_recipients) &
                                                                    Q(parent_message_id=0)))

        query_child_messages = master_data_models.Message.objects.filter(parent_message_id__in=query_inbox.values('id'))

        query_unread_messages_recipients = master_data_models.MessageRecipient.objects.filter(
            Q(message_id__in=query_inbox) & Q(recipient=request.user) & Q(is_read=False) |
            (Q(message_id__in=query_child_messages) & Q(recipient=request.user) & Q(is_read=False)))

        query_unread_messages = master_data_models.Message.objects.filter(id__in=query_unread_messages_recipients.values('message_id'))

        return render(request, 'FlowManagement/InboxItems.html', {'query_inbox': query_inbox,
                                                                  'query_unread_messages':query_unread_messages,
                                                                  'query_unread_messages_recipients':
                                                                      query_unread_messages_recipients})


def load_sent_items(request):
    if request.method == "POST":

        table_sent = sent_items(request)

        return render(request, 'FlowManagement/MessagingComponents.html',{'table': table_sent, "title": "Sent Items"})


def load_trash_items(request):
    if request.method == "POST":

        table_trash = trash_items(request)

        return render(request, 'FlowManagement/MessagingComponents.html',{'table': table_trash, "title": "Trashed Items"})


def delete_from_mail_box(request):
    if request.method == "POST":
        item_pk = int(request.POST["item_pk"])
        model_name = (request.POST["model"])
        app_name = (request.POST["app_name"])

        query_message = master_data_models.Message.objects.get(id=item_pk)

        if request.user == query_message.creator:
            query_message.deleted_from_mail_box = True
            query_message.save()

        model = apps.get_model(app_name, model_name)

        query = model.objects.filter(message_id=item_pk, recipient=request.user)

        for x in query:
            x.deleted_from_mail_box = True
            x.save()

        query_message = master_data_models.Message.objects.get(id=item_pk)

        query_trashed_messages = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                    is_trashed=True,
                                                                                    deleted_from_mail_box=False).values(
            'message')
        table_trash = MessageTrashedTable(
            master_data_models.Message.objects.filter(Q(id__in=query_trashed_messages) |
                                                      Q(trashed_by_creator=True) & Q(deleted_from_mail_box=False) &
                                                      Q(creator=request.user)))

        return render(request, 'FlowManagement/MessagingComponents.html', {'table': table_trash, "title": "Trashed Items"})


def get_jasper_server_instance(request):
    if request.method == "GET":

        url = 'http://178.79.177.52:8080/jasperserver-pro/flow.html?_flowId=searchFlow&mode=search&filterId' \
              '=resourceTypeFilter&filterOption=resourceTypeFilter-adhocView&username=jasperadmin&password=jasperadmin'

        return HttpResponse(url)


def get_auth():
    session = requests.Session()
    response = session.post(elmis_server, params)

    if response.status_code == 200:
        return session.cookies.get_dict()
    else:
        return 'error'


def get_data(cookie, startDate, endDate, program, schedule):
    # r = requests.get(
    #     'https://elmis.co.tz/reports/reportdata/facilityConsumption.json?disaggregated=true&facility=&facilityType='
    #     '&max=10000&pdformat=1&periodEnd='+endDate+'&periodStart='+startDate+'&program=2&zone=437&zoneName='
    #                                                                          'Tanzania+-+Country',sdasdas
    #     params={'q': 'requests+language:python'},
    #     headers={'Cookie': cookie}
    # )
    r = requests.get(
        'https://elmis.co.tz/reports/reportdata/quantification-extract.json?limit=100&max=2000&page=1&'
        'periodEnd='+endDate+'&periodStart='+startDate+'&program='+program+'&schedule='+schedule+'',
        params={'q': 'requests+language:python'},
        headers={'Cookie': cookie}
    )

    if r.status_code == 200:
        return r.json()
    else:
        return 'error'


@background(schedule=60)
def update_consumption_data_from_elmis():
    for program in range(1,3):
        for schedule in range(1,3):
            current_date = datetime.today()
            first_day_of_the_month = current_date.replace(day=1)
            last_day_of_previous_month = first_day_of_the_month - timedelta(days=1)
            first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

            three_months_before_start_date = str(first_day_of_previous_month.date() - relativedelta(months=3))
            end_date = str(last_day_of_previous_month.date())

            consumption_json_data_from_elmis = json.dumps(get_data(cookie, three_months_before_start_date, end_date,
                                                                   str(program), str(schedule)))

            json_array = json.loads(consumption_json_data_from_elmis)

            for entry in json_array["openLmisResponse"]["rows"]:
                if str(entry['facilityCode'] is not None):
                    elmis_facility_code = str(entry['facilityCode'])
                    elmis_product_id = str(entry['code'])

                    if entry['consumption'] is not None:
                        elmis_average_monthly_consumption = int(entry['consumption'])/3
                    else:
                        elmis_average_monthly_consumption = 0

                    query_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter \
                        (location__elims_facility_id="" + elmis_facility_code + "",
                         health_commodity__elims_product_id="" + elmis_product_id + "")

                    if query_commodity_balance.count() > 0:
                        for y in query_commodity_balance:
                            y.quantity_consumed = int(elmis_average_monthly_consumption)
                            y.save()
                    else:
                        pass

cookie = 'JSESSIONID=' + get_auth()['JSESSIONID']

