from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from ..forms import UserProfileForm

import datetime
from django.utils import timezone
import json
from django.conf import settings

from MasterDataManagement import models as master_data_models
from MasterDataManagement import forms as master_data_forms
from FlowManagement import views as flow_management_views

from django.db.models import Count
from django.db.models import Avg
from django.db.models import F

from django.contrib.auth.decorators import login_required
from ..tables import UserTable


def get_login_page(request):
    return render(request, 'UserManagement/Login.html')


@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect(request.META['HTTP_REFERER'])

        else:
            messages.error(request, 'Please correct the error below.')
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'UserManagement/ChangePassword.html', {
            'form': form
        })


@login_required(login_url='/')
def logout_view(request):
    logout(request)
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


def authenticate_user(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None and user.is_authenticated:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')
            elif user.is_staff:
                login(request, user)
                return get_dashboard(request,None, None, None,None)

            else:
                messages.success(request,'Not allowed to access this portal')
                return render(request, 'UserManagement/Login.html')
        else:
            messages.success(request, 'User is not active')
            return render(request, 'UserManagement/Login.html')
    else:
        messages.success(request, 'User name or Password is wrong')
        return render(request, 'UserManagement/Login.html')


@login_required(login_url='/')
def set_changed_password(request):

    if request.POST:
        old_password = request.POST['old_password']
        new_password = request.POST['new_password2']

        user = authenticate(request, username=request.user.username, password=old_password)

        if user is not None and user.is_authenticated:
            logged_user = User.objects.get(username = request.user.username)
            logged_user.set_password(new_password)
            logged_user.save()

            return HttpResponse(status=200)

        else:

            return HttpResponse(status=401)


def get_new_user_page(request):
    # query_profile = user_management_models.Profile.objects.get(user=request.user)
    # form_user = UserProfileForm(instance=query_profile)
    form_user = UserProfileForm()
    return render(request, 'UserManagement/UserProfile.html', {'form_user':form_user})


def get_user_management_page(request):

    query_users = User.objects.all()
    table_users = UserTable(query_users)
    return render(request, 'UserManagement/UserManagement.html', {'table':table_users})


def get_facilities_by_user(request):
    query_facilities = None
    # Countries
    query_location = master_data_models.Location.objects.get(id=request.user.profile.location.id)

    # Regions
    query_location_children = master_data_models.Location.objects.filter(parent=query_location.id)

    if query_location_children.count() > 0:
        # Districts
        query_level_1 = master_data_models.Location.objects.filter(parent__in=query_location_children.values('id'))

        if query_level_1.count() > 0:
            # Facilities
            query_level_2 = master_data_models.Location.objects.filter(parent__in=query_level_1.values('id'))

            if query_level_2.count() > 0:
                query_facilities = query_level_2
            else:
                query_facilities = query_level_1

        else:
            query_facilities = query_location_children
    else:
        # Work around to return a queryset so as to count()
        query_facilities = master_data_models.Location.objects.filter(id=request.user.profile.location.id)

    return query_facilities


def get_children_recursively(parent_location_id):
    final_children = []

    query_all_locations = master_data_models.Location.objects.all()

    for x in query_all_locations:
        if x.parent_id == parent_location_id:
            # add this object to an array
            # children.append({"id": x.id, "text": ""+x.location_name+""})

            if len((get_children_recursively(x.id))) > 0:
                final_children.append(
                    {"id": x.id, "text": "" + x.location_name + "", "inc": (get_children_recursively(x.id))})
            else:
                final_children.append(
                    {"id": x.id, "text": "" + x.location_name + ""})

    return final_children


def get_parent_child_relationship(request):
    json_data = ""
    location_id = request.user.profile.location_id
    query_exact_location = master_data_models.Location.objects.get(id=location_id)
    parent_id = query_exact_location.parent_id
    if parent_id is None:
        parent_id = location_id
    else:
        parent_id = query_exact_location.parent_id
    query_locations = master_data_models.Location.objects.all()

    for x in query_locations:
        if x.id == parent_id:
            children = get_children_recursively(parent_id)
            if len(children) > 0:
                json_data = [{"id": x.id, "text": x.location_name, "inc": children}]
            else:
                pass

    return json.dumps(json_data)


@login_required(login_url='/')
def get_dashboard(request, locations,commodities, date_from, date_to):
    districts = []
    values = []

    if request.user.is_anonymous:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        query_total_commodities = master_data_models.HealthCommodity.objects.all()

        if locations is not None:
            query_total_facilities = master_data_models.Location.objects.filter(location_type='FCT', id__in=locations)
            query_transactions_current_month = master_data_models.HealthCommodityTransactions.objects.filter \
                (date_time_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                 posting_schedule__health_commodity_balance__location__in=locations, is_active=True,
                 quantity_consumed__gt=0)
            if date_from is not None and date_to is not None:
                if commodities is not None:
                    date_time_from = "" + date_from + ""  # The date - 29 Dec 2017
                    date_time_to = "" + date_to + ""  # The date - 29 Dec 2017

                    format_str = '%m/%d/%Y'

                    date_time_from_formatted = datetime.datetime.strptime(date_time_from, format_str)
                    date__time_to_formatted = datetime.datetime.strptime(date_time_to, format_str)

                    date_from_formatted = date_time_from_formatted.date()
                    date_to_formatted = date__time_to_formatted.date()

                    query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=locations, quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted), is_active=True,
                         posting_schedule__health_commodity_balance__health_commodity__in=commodities
                         )

                    facility_list = locations

                    aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,
                         quantity_consumed__gt=0, posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                         date_time_created__range=(date_from_formatted,date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                                'posting_schedule__health_commodity_balance__health_commodity__id') \
                        .annotate(average=Avg('quantity_available')). \
                        annotate(average_consumption=Avg('quantity_consumed')). \
                        annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed')). \
                        order_by('posting_schedule__health_commodity_balance__health_commodity')

                    aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                        (location__in=facility_list, is_active=True,health_commodity__in=commodities,
                         quantity_consumed__gt=0) \
                        .values('location__parent') \
                        .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                        filter(location__in=facility_list, is_active=True, quantity_consumed__gt=0,
                               health_commodity__in=commodities) \
                        .values('health_commodity__health_commodity_name'). \
                        annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    for x in aggregated_transactions_by_district:
                        query_district_name = master_data_models.Location.objects.get \
                            (id=x['location__parent'])
                        districts.append(query_district_name.location_name)
                        values.append(x['ratio'])

                    # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
                    data = [[d, v] for d, v in zip(districts, values)]

                    map_data = json.dumps(data)

                    count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,
                         posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                         date_time_created__range=(date_from_formatted, date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__location__location_name',
                                'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                        .annotate(count=Count('posting_schedule')) \
                        .order_by('-count')

                    aggregated_transactions_by_access_level = aggregated_transactions
                    count_location_transactions_by_access_level = count_location_transactions

                    query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

                    form = master_data_forms.LocationTreeForm()

                    query_message_recipients = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                                  is_trashed=False,
                                                                                                  is_read=False)

                    notifications = flow_management_views.get_dashboard_notification_count(request)

                    unread_messages = notifications[0]
                    scheduled_items = notifications[1]

                    if query_post_commodities is not None:
                        items_found = query_post_commodities.count()
                    else:
                        items_found = 0

                    return render(request, 'UserManagement/DashboardElements.html',
                                  {'query_total_facilities': query_total_facilities,
                                   'query_total_commodities': query_total_commodities,
                                   'query_total_transactions': query_total_transactions,
                                   'query_transactions_current_month':
                                       query_transactions_current_month,
                                   'scheduled_items': scheduled_items,
                                   'form': form, 'aggregated_transactions':
                                       aggregated_transactions_by_access_level,
                                   'aggregated_months_of_stock':aggregated_months_of_stock,
                                   'count_location_transactions':
                                       count_location_transactions_by_access_level,
                                   'tree_values': get_parent_child_relationship(request),
                                   'unread_messages': unread_messages,
                                   'map_data':map_data})
                else:
                    date_time_from = "" + date_from + ""  # The date - 29 Dec 2017
                    date_time_to = "" + date_to + ""  # The date - 29 Dec 2017

                    format_str = '%m/%d/%Y'

                    date_time_from_formatted = datetime.datetime.strptime(date_time_from, format_str)
                    date__time_to_formatted = datetime.datetime.strptime(date_time_to, format_str)

                    date_from_formatted = date_time_from_formatted.date()
                    date_to_formatted = date__time_to_formatted.date()

                    query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=locations, quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted), is_active=True
                         )

                    facility_list = locations

                    aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,
                         quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                                'posting_schedule__health_commodity_balance__health_commodity__id') \
                        .annotate(average=Avg('quantity_available')). \
                        annotate(average_consumption=Avg('quantity_consumed')). \
                        annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed')). \
                        order_by('posting_schedule__health_commodity_balance__health_commodity')

                    aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                        (location__in=facility_list, is_active=True,
                         quantity_consumed__gt=0) \
                        .values('location__parent') \
                        .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                        filter(location__in=facility_list, is_active=True, quantity_consumed__gt=0) \
                        .values('health_commodity__health_commodity_name'). \
                        annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    for x in aggregated_transactions_by_district:
                        query_district_name = master_data_models.Location.objects.get \
                            (id=x['location__parent'])
                        districts.append(query_district_name.location_name)
                        values.append(x['ratio'])

                    # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
                    data = [[d, v] for d, v in zip(districts, values)]

                    map_data = json.dumps(data)

                    count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,
                         date_time_created__range=(date_from_formatted, date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__location__location_name',
                                'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                        .annotate(count=Count('posting_schedule')) \
                        .order_by('-count')

                    aggregated_transactions_by_access_level = aggregated_transactions
                    count_location_transactions_by_access_level = count_location_transactions

                    query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

                    form = master_data_forms.LocationTreeForm()

                    query_message_recipients = master_data_models.MessageRecipient.objects.filter(
                        recipient_id=request.user.id,
                        is_trashed=False,
                        is_read=False)

                    notifications = flow_management_views.get_dashboard_notification_count(request)

                    unread_messages = notifications[0]
                    scheduled_items = notifications[1]

                    # if query_post_commodities is not None:
                    #     items_found = query_post_commodities.count()
                    # else:
                    #     items_found = 0

                    return render(request, 'UserManagement/DashboardElements.html',
                                  {'query_total_facilities': query_total_facilities,
                                   'query_total_commodities': query_total_commodities,
                                   'query_total_transactions': query_total_transactions,
                                   'query_transactions_current_month':
                                       query_transactions_current_month,
                                   'scheduled_items': scheduled_items,
                                   'form': form, 'aggregated_transactions':
                                       aggregated_transactions_by_access_level,
                                   'aggregated_months_of_stock': aggregated_months_of_stock,
                                   'count_location_transactions':
                                       count_location_transactions_by_access_level,
                                   'tree_values': get_parent_child_relationship(request),
                                   'unread_messages': unread_messages,
                                   'map_data': map_data})

            elif commodities is not None and date_from is None and date_to is None:
                query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=locations,
                     posting_schedule__health_commodity_balance__health_commodity__in=commodities
                     )

                facility_list = locations

                aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=facility_list,
                     posting_schedule__health_commodity_balance__health_commodity__in=commodities) \
                    .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                            'posting_schedule__health_commodity_balance__health_commodity__id') \
                    .annotate(average=Avg('quantity_available')). \
                    annotate(average_consumption=Avg('quantity_consumed')). \
                    annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed')). \
                    order_by('posting_schedule__health_commodity_balance__health_commodity')

                aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                    (location__in=facility_list, is_active=True,health_commodity__in=commodities,
                     quantity_consumed__gt=0) \
                    .values('location__parent') \
                    .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                    filter(location__in=facility_list, is_active=True, quantity_consumed__gt=0,
                           health_commodity__in=commodities) \
                    .values('health_commodity__health_commodity_name'). \
                    annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                for x in aggregated_transactions_by_district:
                    query_district_name = master_data_models.Location.objects.get \
                        (id=x['location__parent'])
                    districts.append(query_district_name.location_name)
                    values.append(x['ratio'])

                # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
                data = [[d, v] for d, v in zip(districts, values)]

                map_data = json.dumps(data)

                count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=facility_list,
                     posting_schedule__health_commodity_balance__health_commodity__in=commodities) \
                    .values('posting_schedule__health_commodity_balance__location__location_name',
                            'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                    .annotate(count=Count('posting_schedule')) \
                    .order_by('-count')

                aggregated_transactions_by_access_level = aggregated_transactions
                count_location_transactions_by_access_level = count_location_transactions

                query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

                form = master_data_forms.LocationTreeForm()

                query_message_recipients = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                              is_trashed=False,
                                                                                              is_read=False)

                notifications = flow_management_views.get_dashboard_notification_count(request)

                unread_messages = notifications[0]
                scheduled_items = notifications[1]

                locations = get_parent_child_relationship(request)

                return render(request, 'UserManagement/DashboardElements.html',
                              {'query_total_facilities': query_total_facilities,
                               'query_total_commodities': query_total_commodities,
                               'query_total_transactions': query_total_transactions,
                               'query_transactions_current_month':
                                   query_transactions_current_month,
                               'scheduled_items': scheduled_items,
                               'form': form, 'aggregated_transactions':
                                   aggregated_transactions_by_access_level,
                               'aggregated_months_of_stock':aggregated_months_of_stock,
                               'count_location_transactions':
                                   count_location_transactions_by_access_level,
                               'tree_values': get_parent_child_relationship(request),
                               'map_data': map_data,
                               'unread_messages': unread_messages,
                               'locations':locations})
            else:
                query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=locations
                     )

                facility_list = locations

                aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=facility_list) \
                    .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                            'posting_schedule__health_commodity_balance__health_commodity__id') \
                    .annotate(average=Avg('quantity_available')). \
                    annotate(average_consumption=Avg('quantity_consumed')). \
                    annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed')). \
                    order_by('posting_schedule__health_commodity_balance__health_commodity')

                aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                    (location__in=facility_list, is_active=True,quantity_consumed__gt=0) \
                    .values('location__parent') \
                    .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                    filter(location__in=facility_list, is_active=True, quantity_consumed__gt=0) \
                    .values('health_commodity__health_commodity_name'). \
                    annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                for x in aggregated_transactions_by_district:
                    query_district_name = master_data_models.Location.objects.get \
                        (id=x['location__parent'])
                    districts.append(query_district_name.location_name)
                    values.append(x['ratio'])

                # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
                data = [[d, v] for d, v in zip(districts, values)]

                map_data = json.dumps(data)

                count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=facility_list) \
                    .values('posting_schedule__health_commodity_balance__location__location_name',
                            'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                    .annotate(count=Count('posting_schedule')) \
                    .order_by('-count')

                aggregated_transactions_by_access_level = aggregated_transactions
                count_location_transactions_by_access_level = count_location_transactions

                query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

                form = master_data_forms.LocationTreeForm()

                query_message_recipients = master_data_models.MessageRecipient.objects.filter(
                    recipient_id=request.user.id,
                    is_trashed=False,
                    is_read=False)

                notifications = flow_management_views.get_dashboard_notification_count(request)

                unread_messages = notifications[0]
                scheduled_items = notifications[1]

                locations = get_parent_child_relationship(request)

                return render(request, 'UserManagement/DashboardElements.html',
                              {'query_total_facilities': query_total_facilities,
                               'query_total_commodities': query_total_commodities,
                               'query_total_transactions': query_total_transactions,
                               'query_transactions_current_month':
                                   query_transactions_current_month,
                               'scheduled_items': scheduled_items,
                               'form': form, 'aggregated_transactions':
                                   aggregated_transactions_by_access_level,
                               'aggregated_months_of_stock': aggregated_months_of_stock,
                               'count_location_transactions':
                                   count_location_transactions_by_access_level,
                               'tree_values': get_parent_child_relationship(request),
                               'map_data': map_data,
                               'unread_messages': unread_messages,
                               'locations': locations})

        elif date_from is not None and date_to is not None:
            if commodities is not None:
                facility_list = get_facilities_by_user(request).values('id')
                query_total_facilities = master_data_models.Location.objects.filter(location_type='FCT',
                                                                                    id__in=facility_list)
                date_time_from = "" + date_from + ""  # The date - 29 Dec 2017
                date_time_to = "" + date_to + ""  # The date - 29 Dec 2017

                format_str = '%m/%d/%Y'

                date_time_from_formatted = datetime.datetime.strptime(date_time_from, format_str)
                date__time_to_formatted = datetime.datetime.strptime(date_time_to, format_str)

                date_from_formatted = date_time_from_formatted.date()
                date_to_formatted = date__time_to_formatted.date()

                if get_facilities_by_user(request).count() > 0:
                    facility_list = get_facilities_by_user(request).values('id')

                    query_transactions_current_month = master_data_models.HealthCommodityTransactions.objects.filter \
                        (date_time_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0,
                                                                       microsecond=0),
                         posting_schedule__health_commodity_balance__location__in=facility_list,
                         quantity_consumed__gt=0, posting_schedule__health_commodity_balance__health_commodity__in=commodities )

                    query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list,
                         posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                         quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted)
                         )

                    aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list,
                         posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                         quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                                'posting_schedule__health_commodity_balance__health_commodity__id') \
                        .annotate(average=Avg('quantity_available')). \
                        annotate(average_consumption=Avg('quantity_consumed')). \
                        annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed')). \
                        order_by('posting_schedule__health_commodity_balance__health_commodity')

                    aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                        (location__in=facility_list, is_active=True,health_commodity__in=commodities,
                         quantity_consumed__gt=0) \
                        .values('location__parent') \
                        .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                        filter(location__in=facility_list, is_active=True, quantity_consumed__gt=0,
                               health_commodity__in=commodities) \
                        .values('health_commodity__health_commodity_name'). \
                        annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    for x in aggregated_transactions_by_district:
                        query_district_name = master_data_models.Location.objects.get \
                            (id=x['location__parent'])
                        districts.append(query_district_name.location_name)
                        values.append(x['ratio'])

                    # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
                    data = [[d, v] for d, v in zip(districts, values)]

                    map_data = json.dumps(data)

                    count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list,
                         posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                         quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__location__location_name',
                                'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                        .annotate(count=Count('posting_schedule')) \
                        .order_by('-count')

                    aggregated_transactions_by_access_level = aggregated_transactions
                    count_location_transactions_by_access_level = count_location_transactions

                    query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

                    form = master_data_forms.LocationTreeForm()

                    query_message_recipients = master_data_models.MessageRecipient.objects.filter(
                        recipient_id=request.user.id,
                        is_trashed=False,
                        is_read=False)

                    notifications = flow_management_views.get_dashboard_notification_count(request)

                    unread_messages = notifications[0]
                    scheduled_items = notifications[1]

                    return render(request, 'UserManagement/DashboardElements.html',
                                  {'query_total_facilities': query_total_facilities,
                                   'query_total_commodities': query_total_commodities,
                                   'query_total_transactions': query_total_transactions,
                                   'query_transactions_current_month':
                                       query_transactions_current_month,
                                   'scheduled_items': scheduled_items,
                                   'form': form, 'aggregated_transactions':
                                       aggregated_transactions_by_access_level,
                                   'aggregated_months_of_stock': aggregated_months_of_stock,
                                   'count_location_transactions':
                                       count_location_transactions_by_access_level,
                                   'tree_values': get_parent_child_relationship(request),
                                   'map_data': map_data,
                                   'unread_messages': unread_messages})
            else:
                facility_list = get_facilities_by_user(request).values('id')
                query_total_facilities = master_data_models.Location.objects.filter(location_type='FCT', id__in=facility_list)
                date_time_from = "" + date_from + ""  # The date - 29 Dec 2017
                date_time_to = "" + date_to + ""  # The date - 29 Dec 2017

                format_str = '%m/%d/%Y'

                date_time_from_formatted = datetime.datetime.strptime(date_time_from, format_str)
                date__time_to_formatted = datetime.datetime.strptime(date_time_to, format_str)

                date_from_formatted = date_time_from_formatted.date()
                date_to_formatted = date__time_to_formatted.date()

                if get_facilities_by_user(request).count() > 0:
                    facility_list = get_facilities_by_user(request).values('id')

                    query_transactions_current_month = master_data_models.HealthCommodityTransactions.objects.filter \
                        (date_time_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                         posting_schedule__health_commodity_balance__location__in=facility_list,quantity_consumed__gt=0,)

                    query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list,quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted)
                         )

                    aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list,quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                                'posting_schedule__health_commodity_balance__health_commodity__id') \
                        .annotate(average=Avg('quantity_available')). \
                        annotate(average_consumption=Avg('quantity_consumed')). \
                        annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed')). \
                        order_by('posting_schedule__health_commodity_balance__health_commodity')

                    # aggregated_transactions_by_district = master_data_models.HealthCommodityTransactions.objects.filter \
                    #     (posting_schedule__health_commodity_balance__location__in=facility_list,quantity_consumed__gt=0,
                    #      date_time_created__range=(date_from_formatted, date_to_formatted)) \
                    #     .values('posting_schedule__health_commodity_balance__location__parent'). \
                    #     annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed'))

                    aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                        (location__in=facility_list, is_active=True,
                         quantity_consumed__gt=0) \
                        .values('location__parent') \
                        .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                        filter(location__in=facility_list, is_active=True, quantity_consumed__gt=0) \
                        .values('health_commodity__health_commodity_name'). \
                        annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                    for x in aggregated_transactions_by_district:
                        query_district_name = master_data_models.Location.objects.get \
                            (id=x['location__parent'])
                        districts.append(query_district_name.location_name)
                        values.append(x['ratio'])

                    # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
                    data = [[d, v] for d, v in zip(districts, values)]

                    map_data = json.dumps(data)

                    count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                        (posting_schedule__health_commodity_balance__location__in=facility_list,quantity_consumed__gt=0,
                         date_time_created__range=(date_from_formatted, date_to_formatted)) \
                        .values('posting_schedule__health_commodity_balance__location__location_name',
                                'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                        .annotate(count=Count('posting_schedule')) \
                        .order_by('-count')

                    aggregated_transactions_by_access_level = aggregated_transactions
                    count_location_transactions_by_access_level = count_location_transactions

                    query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

                    form = master_data_forms.LocationTreeForm()

                    query_message_recipients = master_data_models.MessageRecipient.objects.filter(
                        recipient_id=request.user.id,
                        is_trashed=False,
                        is_read=False)

                    notifications = flow_management_views.get_dashboard_notification_count(request)

                    unread_messages = notifications[0]
                    scheduled_items = notifications[1]

                    return render(request, 'UserManagement/DashboardElements.html',
                                  {'query_total_facilities': query_total_facilities,
                                   'query_total_commodities': query_total_commodities,
                                   'query_total_transactions': query_total_transactions,
                                   'query_transactions_current_month':
                                       query_transactions_current_month,
                                   'scheduled_items': scheduled_items,
                                   'form': form, 'aggregated_transactions':
                                       aggregated_transactions_by_access_level,
                                   'aggregated_months_of_stock':aggregated_months_of_stock,
                                   'count_location_transactions':
                                       count_location_transactions_by_access_level,
                                   'tree_values': get_parent_child_relationship(request),
                                   'map_data': map_data,
                                   'unread_messages': unread_messages})

        elif locations is None and date_from is None and date_to is None and commodities is not None:
            facility_list = get_facilities_by_user(request).values('id')
            query_total_facilities = master_data_models.Location.objects.filter(location_type='FCT', id__in=facility_list)
            query_transactions_current_month = master_data_models.HealthCommodityTransactions.objects.filter \
                (date_time_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                 posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,
                 quantity_consumed__gt=0, posting_schedule__health_commodity_balance__health_commodity__in=commodities)

            query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                (posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                 posting_schedule__health_commodity_balance__location__in=facility_list
                 )



            aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                (posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                 posting_schedule__health_commodity_balance__location__in=facility_list
                 ) \
                .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                        'posting_schedule__health_commodity_balance__health_commodity__id') \
                .annotate(average=Avg('quantity_available')). \
                annotate(average_consumption=Avg('quantity_consumed')). \
                annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed')). \
                order_by('posting_schedule__health_commodity_balance__health_commodity')

            aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                (is_active=True, health_commodity__in=commodities, location__in=facility_list,
                 quantity_consumed__gt=0) \
                .values('location__parent') \
                .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

            aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                filter(is_active=True, quantity_consumed__gt=0,location__in=facility_list,
                       health_commodity__in=commodities) \
                .values('health_commodity__health_commodity_name'). \
                annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

            for x in aggregated_transactions_by_district:
                query_district_name = master_data_models.Location.objects.get \
                    (id=x['location__parent'])
                districts.append(query_district_name.location_name)
                values.append(x['ratio'])

            # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
            data = [[d, v] for d, v in zip(districts, values)]

            map_data = json.dumps(data)

            count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                (posting_schedule__health_commodity_balance__health_commodity__in=commodities,
                 posting_schedule__health_commodity_balance__location__in=facility_list
                 ) \
                .values('posting_schedule__health_commodity_balance__location__location_name',
                        'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                .annotate(count=Count('posting_schedule')) \
                .order_by('-count')

            aggregated_transactions_by_access_level = aggregated_transactions
            count_location_transactions_by_access_level = count_location_transactions

            query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

            form = master_data_forms.LocationTreeForm()

            query_message_recipients = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                          is_trashed=False,
                                                                                          is_read=False)

            notifications = flow_management_views.get_dashboard_notification_count(request)

            unread_messages = notifications[0]
            scheduled_items = notifications[1]

            locations = get_parent_child_relationship(request)

            return render(request, 'UserManagement/DashboardElements.html',
                          {'query_total_facilities': query_total_facilities,
                           'query_total_commodities': query_total_commodities,
                           'query_total_transactions': query_total_transactions,
                           'query_transactions_current_month':
                               query_transactions_current_month,
                           'scheduled_items': scheduled_items,
                           'form': form, 'aggregated_transactions':
                               aggregated_transactions_by_access_level,
                           'aggregated_months_of_stock': aggregated_months_of_stock,
                           'count_location_transactions':
                               count_location_transactions_by_access_level,
                           'tree_values': get_parent_child_relationship(request),
                           'map_data': map_data,
                           'unread_messages': unread_messages,
                           'locations': locations})

        elif locations is None and date_from is None and date_to is None and commodities is None:
            facility_list = get_facilities_by_user(request).values('id')
            query_total_facilities = master_data_models.Location.objects.filter(location_type='FCT', id__in=facility_list)
            aggregated_transactions_by_access_level  = None
            count_location_transactions_by_access_level = None
            map_data = None

            if get_facilities_by_user(request).count() > 0:
                facility_list = get_facilities_by_user(request).values('id')

                query_total_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,quantity_consumed__gt=0)
                query_transactions_current_month = master_data_models.HealthCommodityTransactions.objects.filter \
                    (date_time_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                     posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,quantity_consumed__gt=0)

                aggregated_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,quantity_consumed__gt=0) \
                    .values('posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
                            'posting_schedule__health_commodity_balance__health_commodity__id') \
                    .annotate(average=Avg('quantity_available')). \
                    annotate(average_consumption=Avg('quantity_consumed')). \
                    annotate(ratio=Avg('quantity_available')/Avg('quantity_consumed')). \
                    order_by('posting_schedule__health_commodity_balance__health_commodity')

                aggregated_transactions_by_district = master_data_models.HealthCommodityBalance.objects.filter \
                    (location__in=facility_list, is_active=True,
                     quantity_consumed__gt=0) \
                    .values('location__parent') \
                    .annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                aggregated_months_of_stock = master_data_models.HealthCommodityBalance.objects. \
                    filter(location__in=facility_list, is_active=True, quantity_consumed__gt=0) \
                    .values('health_commodity__health_commodity_name'). \
                    annotate(ratio=Avg(F('quantity_available') / F('quantity_consumed')))

                for x in aggregated_transactions_by_district:
                    query_district_name = master_data_models.Location.objects.get \
                        (id=x['location__parent'])
                    districts.append(query_district_name.location_name)
                    values.append(x['ratio'])

                data = [[d, v] for d, v in zip(districts, values)]

                map_data = json.dumps(data)

                count_location_transactions = master_data_models.HealthCommodityTransactions.objects.filter \
                    (posting_schedule__health_commodity_balance__location__in=facility_list, is_active=True,quantity_consumed__gt=0) \
                    .values('posting_schedule__health_commodity_balance__location__location_name',
                            'posting_schedule__health_commodity_balance__location__facility_type__facility_type_description') \
                    .annotate(count=Count('posting_schedule')) \
                    .order_by('-count')

                aggregated_transactions_by_access_level = aggregated_transactions
                count_location_transactions_by_access_level = count_location_transactions

                query_post_commodities = flow_management_views.check_for_commodities_to_post(request)

                form = master_data_forms.LocationTreeForm()

                query_message_recipients = master_data_models.MessageRecipient.objects.filter(recipient_id=request.user.id,
                                                                                              is_trashed=False, is_read=False)

                notifications = flow_management_views.get_dashboard_notification_count(request)

                unread_messages = notifications[0]
                scheduled_items = notifications[1]

                locations = get_parent_child_relationship(request)

                query_health_commodities = master_data_models.HealthCommodity.objects.values("id","health_commodity_name")

                return render(request, 'UserManagement/Dashboard/index.html', {'query_total_facilities':query_total_facilities,
                                                                               'query_total_commodities':query_total_commodities,
                                                                               'query_total_transactions':query_total_transactions,
                                                                               'query_transactions_current_month':
                                                                                   query_transactions_current_month,
                                                                               'scheduled_items':scheduled_items,
                                                                               'form':form, 'aggregated_transactions':
                                                                                   aggregated_transactions_by_access_level,
                                                                               'aggregated_months_of_stock':
                                                                                   aggregated_months_of_stock,
                                                                               'count_location_transactions':
                                                                                   count_location_transactions_by_access_level,
                                                                               'unread_messages':unread_messages,
                                                                               'map_data':map_data,
                                                                               'locations':locations,
                                                                               'query_health_commodities':
                                                                                   query_health_commodities})


def filter_dashboard(request):
    if request.method == "POST":
        location_array = request.POST["locations"].split(',')
        commodities_array = request.POST["commodities"].split(',')
        date_from = request.POST["date_from"]
        date_to = request.POST["date_to"]

        locations = []

        if commodities_array[0] == "":
            commodities = None
        else:
            commodities = commodities_array

        if location_array[0] == "":
            locations = None
        else:
            for x in location_array:
                facilities = get_facilities_by_location(x)

                for x in facilities:
                    locations.append(x.id)

        if date_from == "":
            date_from = None
        else:
            date_from = request.POST["date_from"]
        if date_to =="":
            date_to = None
        else:
            date_to = request.POST["date_to"]
    else:
        locations = None
        commodities = None
        date_from = None
        date_to = None

    path = get_dashboard(request, locations,commodities ,date_from, date_to)

    return HttpResponse(path)


def get_facilities_by_location(location_id):
    query_location = master_data_models.Location.objects.get(id=location_id)

    # Regions
    query_location_children = master_data_models.Location.objects.filter(parent=query_location.id)

    if query_location_children.count() > 0:
        # Districts
        query_level_1 = master_data_models.Location.objects.filter(parent__in=query_location_children.values('id'))

        if query_level_1.count() > 0:
            # Facilities
            query_level_2 = master_data_models.Location.objects.filter(parent__in=query_level_1.values('id'))

            if query_level_2.count() > 0:
                query_facilities = query_level_2
            else:
                query_facilities = query_level_1

        else:
            query_facilities = query_location_children
    else:
        # Work around to return a queryset so as to count()
        query_facilities = master_data_models.Location.objects.filter(id=location_id)

    return query_facilities


def get_district_severity_data(request):
    districts = []
    values = []

    if get_facilities_by_user(request).count() > 0:
        facility_list = get_facilities_by_user(request).values('id')

        aggregated_transactions_by_district = master_data_models.HealthCommodityTransactions.objects.filter \
            (posting_schedule__health_commodity_balance__location__in=facility_list) \
            .values('posting_schedule__health_commodity_balance__location__parent'). \
            annotate(ratio=Avg('quantity_available') / Avg('quantity_consumed'))

        for x in aggregated_transactions_by_district:
            query_district_name = master_data_models.Location.objects.get \
                (id=x['posting_schedule__health_commodity_balance__location__parent'])
            districts.append(query_district_name.location_name)
            values.append(x['ratio'])

        # data = [{"district":d, "value":v} for d, v in zip(districts, values)]
        data = [[d, v] for d, v in zip(districts, values)]

        json_data = json.dumps(data)

        return json_data




