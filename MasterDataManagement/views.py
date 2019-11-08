from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .tables import HealthCommoditiesTable, HealthCommodityCategoriesTable, UnitsTable, HealthCommodityBalanceTable, \
    ManageHealthCommoditiesTable, PostingFrequencyTable, LocationTable, PostStockBalanceTable, PostConsumptionTable
from .models import HealthCommodity, HealthCommoditiesCategory, Unit, HealthCommodityBalance, \
    PostingFrequency, PostingSchedule, HealthCommodityTransactions, Location
from .forms import HealthCommodityForm, HealthCommodityCategoryForm, UnitForm, HealthCommodityBalanceForm, \
    PostFrequencyForm, UploadFileForm, eLIMSLogin, LocationForm

from django.apps import apps


from FlowManagement import tables as flow_management_tables
from UserManagement.views import main as user_management_views

import django_excel as excel
import traceback

from FlowManagement import views as flow_management_views
from MasterDataManagement import models as master_data_models
from datetime import datetime
from datetime import timedelta
from django.db.models import Avg, Q
from datetime import date
import datetime
import xlwt


def get_health_commodity_categories_page(request):
    table = HealthCommodityCategoriesTable(HealthCommoditiesCategory.objects.filter(is_active=True))
    form = HealthCommodityCategoryForm()

    # RequestConfig(request, paginate={'per_page': 25}).configure(table)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'MasterDataManagement/HealthCommodityCategories.html', {'table': table, 'form':form,
                                                                                   'unread_messages':unread_messages,
                                                                                   'scheduled_items':scheduled_items})


def get_health_commodities_page(request):
    table = HealthCommoditiesTable(HealthCommodity.objects.filter(is_active=True))
    form = HealthCommodityForm()
    form_mapping = HealthCommodityBalanceForm(initial={"location":request.user.profile.location})

    # RequestConfig(request, paginate={'per_page': 25}).configure(table)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'MasterDataManagement/HealthCommodities.html', {'table': table, 'form':form,
                                                                           'form_mapping':form_mapping,
                                                                           'unread_messages':unread_messages,
                                                                           'scheduled_items':scheduled_items})


def get_post_stock_on_hand_page(request):
    facility_list = user_management_views.get_facilities_by_user(request).values('id')

    table = PostStockBalanceTable(HealthCommodityBalance.objects.filter(quantity_available__isnull=True,
                                                                        health_commodity__is_active=True,
                                                                        location__in=facility_list))

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'MasterDataManagement/PostStockOnHand.html', {'table': table, 'unread_messages':unread_messages,
                                                                         'scheduled_items':scheduled_items})


def get_post_consumption_page(request):
    facility_list = user_management_views.get_facilities_by_user(request).values('id')

    query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter(
        location__in=facility_list, health_commodity__is_active=True).order_by('health_commodity')

    table = PostConsumptionTable(query_health_commodity_balance)

    # RequestConfig(request, paginate={'per_page': 25}).configure(table)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    locations = user_management_views.get_parent_child_relationship(request)

    return render(request, 'MasterDataManagement/PostConsumptionFromELIMS.html', {'table': table,
                                                                                  'unread_messages':unread_messages,
                                                                                  'scheduled_items':scheduled_items,
                                                                                  'locations':locations})


def get_post_consumption_page_by_facility(request, item_pk):
    query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter(
        location=item_pk, health_commodity__is_active=True).order_by('health_commodity')

    table = PostConsumptionTable(query_health_commodity_balance)

    # RequestConfig(request, paginate={'per_page': 25}).configure(table)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    locations = user_management_views.get_parent_child_relationship(request)

    return render(request, 'MasterDataManagement/PostConsumptionFromELIMS.html', {'table': table,
                                                                                  'unread_messages':unread_messages,
                                                                                  'scheduled_items':scheduled_items,
                                                                                  'locations':locations})


def get_location_page(request):
    table = LocationTable(Location.objects.filter(is_active=True).order_by('id'))

    form_locations = LocationForm()

    # RequestConfig(request, paginate={'per_page': 25}).configure(table)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'MasterDataManagement/LocationManagement.html', {'table': table,
                                                                            'form_locations':form_locations,
                                                                            'unread_messages':unread_messages,
                                                                            'scheduled_items':scheduled_items})


def update_health_commodity(request, item_pk):
    query_commodity = HealthCommodity.objects.get(id=item_pk)
    form = HealthCommodityForm(instance=query_commodity)

    if request.method == "POST":
        if request.POST:
            form_update_commodity = HealthCommodityForm(request.POST, instance=query_commodity)
            if form_update_commodity.is_valid():
                form_update_commodity.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Health Commodity"
        url = "update_commodity"

        return render(request, 'MasterDataManagement/UpdateItem.html', {'form': form, 'header': header,
                                                                        'item_pk':item_pk, "url":url
                                                                        })
    return redirect(request.META['HTTP_REFERER'])


def update_health_commodity_category(request, item_pk):
    query_commodity_category = HealthCommoditiesCategory.objects.get(id=item_pk, is_active=True)
    form = HealthCommodityCategoryForm(instance=query_commodity_category)

    if request.method == "POST":
        if request.POST:
            form_update_category = HealthCommodityCategoryForm(request.POST, instance=query_commodity_category)
            if form_update_category.is_valid():
                form_update_category.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Category"
        url = "update_category"
        return render(request, 'MasterDataManagement/UpdateItem.html', {'form': form, 'header': header,
                                                                        'item_pk': item_pk, "url": url})

    return redirect(request.META['HTTP_REFERER'])


def update_unit(request, item_pk):
    query_unit = Unit.objects.get(id=item_pk)
    form = UnitForm(instance=query_unit)

    if request.method == "POST":
        if request.POST:
            form_update_unit = UnitForm(request.POST, instance=query_unit)
            if form_update_unit.is_valid():
                form_update_unit.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Unit"
        url = "update_unit"
        return render(request, 'MasterDataManagement/UpdateItem.html', {'form': form, 'header':header,
                                                                        'item_pk':item_pk, "url":url})

    return redirect(request.META['HTTP_REFERER'])


def update_location(request, item_pk):
    query_location = Location.objects.get(id=item_pk)
    form = LocationForm(instance=query_location)

    if request.method == "POST":
        if request.POST:
            form_update_location = LocationForm(request.POST, instance=query_location)
            if form_update_location.is_valid():
                form_update_location.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Location"
        url = "update_location"
        return render(request, 'MasterDataManagement/UpdateItem.html', {'form': form, 'header':header,
                                                                        'item_pk':item_pk, "url":url})

    return redirect(request.META['HTTP_REFERER'])


def update_frequency(request, item_pk):
    query_frequency = PostingFrequency.objects.get(id=item_pk)
    form_frequency = PostFrequencyForm(instance=query_frequency)

    if request.method == "POST":
        if request.POST:
            form_frequency = PostFrequencyForm(request.POST, instance=query_frequency)
            if form_frequency.is_valid():
                form_frequency.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Frequency"
        url = "update_frequency"
        return render(request, 'MasterDataManagement/UpdateItem.html', {'form': form_frequency,'header':header,
                                                                        'item_pk':item_pk, "url":url})

    return redirect(request.META['HTTP_REFERER'])


def update_mapping(request, item_pk):
    query_mapping = HealthCommodityBalance.objects.get(id=item_pk)
    form_mapping = HealthCommodityBalanceForm(instance=query_mapping)

    if request.method == "POST":
        if request.POST:
            form_mapping = HealthCommodityBalanceForm(request.POST, instance=query_mapping)
            if form_mapping.is_valid():
                form_mapping.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                pass
    else:
        header = "Update Mapping"
        url = "update_mapping"
        return render(request, 'MasterDataManagement/UpdateItem.html', {'form': form_mapping, 'header':header,
                                                                        'item_pk': item_pk, "url":url})


def get_units_page(request):
    table = UnitsTable(Unit.objects.filter(is_active=True))
    form = UnitForm()

    # RequestConfig(request, paginate={'per_page': 25}).configure(table)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'MasterDataManagement/Units.html', {'table': table, 'form':form, 'unread_messages':unread_messages,
                                                               'scheduled_items':scheduled_items})


def get_frequency_page(request):
    table = PostingFrequencyTable(PostingFrequency.objects.filter(is_active=True))
    form = PostFrequencyForm()

    # RequestConfig(request, paginate={'per_page': 25}).configure(table)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render(request, 'MasterDataManagement/PostingFrequencies.html', {'table': table, 'form':form,
                                                                            'unread_messages':unread_messages,
                                                                            'scheduled_items':scheduled_items})


def get_new_mappings_page(request):

    query_categories = HealthCommoditiesCategory.objects.filter(is_active=True)

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    return render (request, 'MasterDataManagement/NewMappings.html', {'query_categories':query_categories,
                                                                      'unread_messages':unread_messages,
                                                                      'scheduled_items':scheduled_items})


def get_commodity_facility_mappings_page(request):
    facility_list = user_management_views.get_facilities_by_user(request).values('id')

    query_health_commodity_balance = master_data_models.HealthCommodityBalance.objects.filter(
        location__in=facility_list, health_commodity__is_active=True).order_by('health_commodity')

    unmanaged_commodities = query_health_commodity_balance.values('health_commodity')

    query_unmanaged_health_commodities = HealthCommodity.objects.exclude(Q(id__in=unmanaged_commodities))

    query_categories = HealthCommoditiesCategory.objects.filter(is_active=True)

    table_managed_commodities = HealthCommodityBalanceTable(query_health_commodity_balance)

    table_unmanaged_commodities = ManageHealthCommoditiesTable(query_unmanaged_health_commodities)

    form_elims = eLIMSLogin()

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    locations = master_data_models.Location.objects.filter(parent=request.user.profile.location_id)

    return render(request, 'MasterDataManagement/CommodityFacilityMappings.html', {
        'table_managed_commodities':table_managed_commodities,
        'table_unmanaged_commodities':table_unmanaged_commodities,
        'query_categories':query_categories,
        'form':form_elims, 'unread_messages':unread_messages, 'scheduled_items':scheduled_items, 'locations':locations
    })


def get_unmanaged_commodities_by_facility(request, item_pk):

    # For district level
    query_health_commodity_balance_by_facility = master_data_models.HealthCommodityBalance.objects.filter(
        location=item_pk, health_commodity__is_active=True).order_by('health_commodity')

    unmanaged_commodities_by_facility = query_health_commodity_balance_by_facility.values('health_commodity')

    query_unmanaged_health_commodities_by_facility = HealthCommodity.objects.exclude(Q(id__in=unmanaged_commodities_by_facility))

    query_categories = HealthCommoditiesCategory.objects.filter(is_active=True)

    table_unmanaged_commodities = ManageHealthCommoditiesTable(query_unmanaged_health_commodities_by_facility)

    form_elims = eLIMSLogin()

    notifications = flow_management_views.get_dashboard_notification_count(request)

    unread_messages = notifications[0]
    scheduled_items = notifications[1]

    locations = master_data_models.Location.objects.filter(parent=request.user.profile.location_id)

    return render(request, 'MasterDataManagement/UnmanagedHealthCommodities.html', {
        'table_unmanaged_commodities':table_unmanaged_commodities,
        'query_categories':query_categories,
        'form':form_elims, 'unread_messages':unread_messages, 'scheduled_items':scheduled_items, 'locations':locations,
        'item_pk':item_pk
    })


def save_mappings(request):
    if request.method == "POST":
        pks = request.POST.getlist("is_managed")
        selected_commodities = HealthCommodity.objects.filter(pk__in=pks)

        for x in selected_commodities:
            instance_balance = HealthCommodityBalance()
            instance_balance.health_commodity_id = x.id
            instance_balance.user_created = request.user
            instance_balance.location = request.user.profile.location
            instance_balance.save()

            create_posting_scheduled_for_mapping_created(instance_balance.id)

    return redirect(request.META['HTTP_REFERER'])


def save_mappings_by_facility(request):
    if request.method == "POST":
        pks = request.POST.getlist("is_managed")
        item_pk = request.POST["facility_id"]

        print(item_pk)
        print(pks)

        selected_commodities = HealthCommodity.objects.filter(pk__in=pks)

        for x in selected_commodities:
            instance_balance = HealthCommodityBalance()
            instance_balance.health_commodity_id = x.id
            instance_balance.user_created = request.user
            instance_balance.location_id = int(item_pk)
            instance_balance.save()

            create_posting_scheduled_for_mapping_created(instance_balance.id)

        return redirect(request.META['HTTP_REFERER'])


def save_stock_on_hand(request):
    if request.method == "POST":
        pks = request.POST.getlist("record_id")
        qty_available = request.POST.getlist("id_quantity_available")
        i = 0

        selected_commodity_balance = HealthCommodityBalance.objects.filter(pk__in=pks)

        for x in selected_commodity_balance:
            qty = qty_available[i]
            x.quantity_available = qty
            x.save()

            i += 1

    return redirect(request.META['HTTP_REFERER'])


def save_consumption(request):
    if request.method == "POST":
        pks = request.POST.getlist("record_id")
        qty_consumed = request.POST.getlist("id_quantity_consumed")
        i = 0

        selected_commodity_balance = HealthCommodityBalance.objects.filter(pk__in=pks)

        for x in selected_commodity_balance:
            qty = qty_consumed[i]

            # reporting_period = round(30/x.health_commodity.posting_frequency.number_of_days)
            if qty is not None:
                # x.quantity_consumed = int(qty)/reporting_period
                x.quantity_consumed = qty
                x.save()

            i += 1

    return redirect(request.META['HTTP_REFERER'])


def save_new_commodity(request):
    if request.POST:
        form = HealthCommodityForm(request.POST)

    if form.is_valid():
        form.full_clean()
        instance = form.save(commit=False)
        instance.save()

        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('.')


def save_new_facility(request):
    if request.POST:
        form = LocationForm(request.POST)

        if form.is_valid():
            form.full_clean()
            instance = form.save(commit=False)
            instance.save()

            return redirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse('.')


def save_new_category(request):
    if request.POST:
        form = HealthCommodityCategoryForm(request.POST)

    if form.is_valid():
        form.full_clean()
        instance = form.save(commit=False)
        instance.save()

        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('.')


def save_new_unit(request):
    if request.POST:
        form = UnitForm(request.POST)

    if form.is_valid():
        form.full_clean()
        instance = form.save(commit=False)
        instance.save()

        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('.')


def save_new_frequency(request):
    if request.POST:
        form = PostFrequencyForm(request.POST)

    if form.is_valid():
        form.full_clean()
        instance = form.save(commit=False)
        instance.save()

        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('.')


def delete_item(request):
    if request.method == "POST":
        item_pk = int(request.POST["item_pk"])
        model_name = (request.POST["model"])
        app_name = (request.POST["app_name"])

        model = apps.get_model(app_name, model_name)

        query = model.objects.get(id=item_pk)
        query.delete()

        return redirect(request.META['HTTP_REFERER'])


def disable_item(request):
    if request.method == "POST":
        item_pk = int(request.POST["item_pk"])
        model_name = (request.POST["model"])
        app_name = (request.POST["app_name"])

        model = apps.get_model(app_name, model_name)

        query = model.objects.get(id=item_pk)
        query.is_active = False
        query.save()

        # Schedule records for the deactivated mappiing should disable the schedule also
        if model_name == "HealthCommodityBalance":
            query_posting = PostingSchedule.objects.filter(health_commodity_balance_id=item_pk)

            for x in query_posting:
                x.is_active = False
                x.save()

        return redirect(request.META['HTTP_REFERER'])


def export_sheet(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(Location, 'xls', status=200, file_name="Locations")
    elif atype == "book":
        return excel.make_response_from_tables(
            [Location], 'xls', file_name="Locations")
    elif atype == "custom":
        query_sets = Location.objects.all()
        column_names = ['location_name','common_name','location_type']
        return excel.make_response_from_query_sets(
            query_sets,
            column_names,
            'xls',
            file_name="Locations"
        )
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=1,
                model=Location,
                mapdict=['location_name','common_name','location_type']
            )
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,'MasterDataManagement/UploadFile.html', {'form': form})


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_handle = request.FILES['file']
            return excel.make_response(file_handle.get_sheet(), "csv")
        else:
            print(traceback.print_stack(f=None, limit=None, file=None))
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request,'MasterDataManagement/UploadFile.html',
                  {'form': form})


def create_posting_scheduled_for_mapping_created(health_commodity_balance_id):

    if health_commodity_balance_id is not None:
        query_commodity_balance = HealthCommodityBalance.objects.get(id=health_commodity_balance_id)

        query_commodity = HealthCommodity.objects.get(id=query_commodity_balance.
                                                      health_commodity_id)

        if query_commodity is not None:
            monthly_posting_count = round(30 / query_commodity.posting_frequency.number_of_days)

            for i in range(0, monthly_posting_count):
                instance_schedule = PostingSchedule()

                calculated_date = date.today() + timedelta(days=(i * query_commodity.
                                                                 posting_frequency.number_of_days))
                query_post_schedule = PostingSchedule.objects.filter(scheduled_date=calculated_date,
                                                                     health_commodity_balance_id=health_commodity_balance_id)

                if query_post_schedule.count() == 0:
                    if calculated_date.weekday() == 5:
                        postponed_date = date.today() + timedelta(days=(i * query_commodity.
                                                                        posting_frequency.
                                                                        number_of_days) + 2)
                        query_postponed_date = PostingSchedule.objects.filter(scheduled_date=postponed_date,
                                                                              health_commodity_balance_id=health_commodity_balance_id)

                        if query_postponed_date.count() == 0:
                            instance_schedule.scheduled_date = date.today() + timedelta(
                                days=(i * query_commodity.
                                      posting_frequency.
                                      number_of_days) + 2)
                            instance_schedule.health_commodity_balance_id = health_commodity_balance_id
                            instance_schedule.save()

                    elif calculated_date.weekday() == 6:
                        postponed_date = date.today() + timedelta(days=(i * query_commodity.
                                                                        posting_frequency.
                                                                        number_of_days) + 1)
                        query_postponed_date = PostingSchedule.objects.filter(scheduled_date=postponed_date,
                                                                              health_commodity_balance_id=health_commodity_balance_id)

                        if query_postponed_date.count() == 0:
                            instance_schedule.scheduled_date = date.today() + timedelta(
                                days=(i * query_commodity.
                                      posting_frequency.
                                      number_of_days) + 1)
                            instance_schedule.health_commodity_balance_id = health_commodity_balance_id
                            instance_schedule.save()

                    elif calculated_date.weekday() != 5 or calculated_date.weekday() != 6:
                        instance_schedule.scheduled_date = calculated_date
                        instance_schedule.health_commodity_balance_id = health_commodity_balance_id
                        instance_schedule.save()
                    else:
                        pass

                else:
                    pass


def create_schedule_for_commodity_posted(posting_schedule_id):

    if posting_schedule_id is not None:
        query_posting_schedule = PostingSchedule.objects.get(id=posting_schedule_id)

        # Get the commidty details
        query_commodity = query_posting_schedule.health_commodity_balance.health_commodity

        query_posting_date = PostingSchedule.objects.filter(
            health_commodity_balance_id=query_posting_schedule.health_commodity_balance_id, status="pending"). \
            order_by('-scheduled_date')

        if query_posting_date is not None:
            query_last_scheduled_date = query_posting_date[0]
            query_next_scheduled_date = query_posting_date.reverse()[0]

            if query_next_scheduled_date is not None and query_last_scheduled_date is not None:
                delta = query_last_scheduled_date.scheduled_date - query_next_scheduled_date.scheduled_date

                diff_in_days = delta.days

                # Schedule for the whole month is there
                if diff_in_days == 30:
                    pass
                else:
                    days_missing_in_schedule = 30 - diff_in_days

                    if days_missing_in_schedule >= query_commodity.posting_frequency.number_of_days:
                        monthly_posting_count = round(
                            days_missing_in_schedule / query_commodity.posting_frequency.number_of_days)

                        for i in range(1, monthly_posting_count):
                            calculated_date = query_last_scheduled_date.scheduled_date + timedelta(
                                days=(i * query_commodity.
                                      posting_frequency.
                                      number_of_days))

                            instance_schedule = PostingSchedule()
                            query_post_schedule = PostingSchedule.objects.filter(
                                scheduled_date=calculated_date,
                                health_commodity_balance_id=query_posting_schedule.health_commodity_balance_id)
                            if query_post_schedule.count() == 0:
                                if calculated_date.weekday() == 5:
                                    postponed_date = date.today() + timedelta(
                                        days=(i * query_commodity.
                                              posting_frequency.
                                              number_of_days) + 2)
                                    query_postponed_date = PostingSchedule.objects.filter(
                                        scheduled_date=postponed_date,
                                        health_commodity_balance_id=query_posting_schedule.health_commodity_balance_id)

                                    if query_postponed_date.count == 0:
                                        instance_schedule.scheduled_date = date.today() + timedelta(
                                            days=x.health_commodity.
                                                     posting_frequency.number_of_days + 2)
                                        instance_schedule.health_commodity_balance_id = query_posting_schedule.health_commodity_balance_id
                                        instance_schedule.save()

                                elif calculated_date.weekday() == 6:
                                    postponed_date = date.today() + timedelta(
                                        days=(i * query_commodity.
                                              posting_frequency.
                                              number_of_days) + 1)
                                    query_postponed_date = PostingSchedule.objects.filter(
                                        scheduled_date=postponed_date,
                                        health_commodity_balance_id=query_posting_schedule.health_commodity_balance_id)

                                    if query_postponed_date.count == 0:
                                        instance_schedule.scheduled_date = date.today() + timedelta(
                                            days=x.health_commodity.
                                                     posting_frequency.
                                                     number_of_days + 1)
                                    instance_schedule.health_commodity_balance_id = query_posting_schedule.health_commodity_balance_id
                                    instance_schedule.save()

                                else:
                                    instance_schedule.scheduled_date = calculated_date
                                    instance_schedule.health_commodity_balance_id = query_posting_schedule.health_commodity_balance_id
                                    instance_schedule.save()
                            else:
                                pass

        else:
            monthly_posting_count = round(30 / query_commodity.posting_frequency.number_of_days)

            for i in range(1, monthly_posting_count):
                instance_schedule = PostingSchedule()

                calculated_date = date.today() + timedelta(days=query_commodity.
                                                           posting_frequency.number_of_days)
                query_post_schedule = PostingSchedule.objects.filter(
                    scheduled_date=calculated_date,
                    health_commodity_balance_id=query_posting_schedule.health_commodity_balance_id)

                if query_post_schedule.count() == 0:
                    if calculated_date.weekday() == 5:
                        postponed_date = date.today() + timedelta(days=(i * query_commodity.
                                                                        posting_frequency.
                                                                        number_of_days) + 2)
                        query_postponed_date = PostingSchedule.objects.filter(
                            scheduled_date=postponed_date,
                            health_commodity_balance_id=query_posting_schedule.health_commodity_balance_id)

                        if query_postponed_date.count == 0:
                            instance_schedule.scheduled_date = date.today() + timedelta(
                                days=query_commodity.
                                         posting_frequency.
                                         number_of_days + 2)
                            instance_schedule.health_commodity_balance_id = query_posting_schedule.health_commodity_balance_id
                            instance_schedule.save()

                    elif calculated_date.weekday() == 6:
                        postponed_date = date.today() + timedelta(days=(i * query_commodity.
                                                                        posting_frequency.
                                                                        number_of_days) + 1)
                        query_postponed_date = PostingSchedule.objects.filter(
                            scheduled_date=postponed_date,
                            health_commodity_balance_id=query_posting_schedule.health_commodity_balance_id)

                        if query_postponed_date.count == 0:
                            instance_schedule.scheduled_date = date.today() + timedelta(
                                days=x.health_commodity.
                                         posting_frequency.
                                         number_of_days + 1)
                            instance_schedule.health_commodity_balance_id = query_posting_schedule.health_commodity_balance_id
                            instance_schedule.save()

                    elif calculated_date.weekday() != 5 or calculated_date.weekday() != 6:
                        instance_schedule.scheduled_date = calculated_date
                        instance_schedule.health_commodity_balance_id = query_posting_schedule.health_commodity_balance_id
                        instance_schedule.save()

                    else:
                        pass
                else:
                    pass


def filter_scheduled_transactions(request):
    if request.method == "POST":
        location_array = request.POST["locations"].split(',')
        date_from = request.POST["date_from"]
        date_to = request.POST["date_to"]

        locations = []

        if location_array[0] == "" or location_array is None:
            locations = None
        else:
            for x in location_array:
                facilities = user_management_views.get_facilities_by_location(x)

                for x in facilities:
                    locations.append(x.id)

        query_schedule = master_data_models.PostingSchedule.objects.all()

        if locations is not None:
            if date_from == "" and date_to == "":
                query_schedule = master_data_models.PostingSchedule.objects.filter \
                    (health_commodity_balance__location__in=locations)
            else:
                date_time_from = "" + date_from + ""  # The date - 29 Dec 2017
                date_time_to = "" + date_to + ""  # The date - 29 Dec 2017

                format_str = '%m/%d/%Y'

                date_time_from_formatted = datetime.datetime.strptime(date_time_from, format_str)
                date__time_to_formatted = datetime.datetime.strptime(date_time_to, format_str)

                date_from_formatted = date_time_from_formatted.date()
                date_to_formatted = date__time_to_formatted.date()

                query_schedule = master_data_models.PostingSchedule.objects.filter(
                    health_commodity_balance__location__in=locations,
                    scheduled_date__range=(date_from_formatted, date_to_formatted))

        elif locations is None and date_from != "" and date_to != "":
            date_time_from = "" + date_from + ""  # The date - 29 Dec 2017
            date_time_to = "" + date_to + ""  # The date - 29 Dec 2017

            format_str = '%m/%d/%Y'

            date_time_from_formatted = datetime.datetime.strptime(date_time_from, format_str)
            date__time_to_formatted = datetime.datetime.strptime(date_time_to, format_str)

            date_from_formatted = date_time_from_formatted.date()
            date_to_formatted = date__time_to_formatted.date()

            query_schedule = master_data_models.PostingSchedule.objects.filter(
                scheduled_date__range=(date_from_formatted, date_to_formatted))

        table_scheduled_transactions = flow_management_tables.ScheduledTransactionTable(query_schedule)

        return render(request, 'MasterDataManagement/ScheduleTable.html',
                      {'table_scheduled_transactions': table_scheduled_transactions})


def export_posted_transactions_xls(request,date_from, date_to):
    facility_list = user_management_views.get_facilities_by_user(request).values('id')

    if date_from is not None and date_to is not None:
        date_time_from = "" + date_from + ""  # The date - 29 Dec 2017
        date_time_to = "" + date_to + ""  # The date - 29 Dec 2017

        format_str = '%m-%d-%Y'

        date_time_from_formatted = datetime.datetime.strptime(date_time_from, format_str)
        date__time_to_formatted = datetime.datetime.strptime(date_time_to, format_str)

        date_from_formatted = date_time_from_formatted.date()
        date_to_formatted = date__time_to_formatted.date()

        query_transactions = HealthCommodityTransactions.objects.filter(date_time_created__range=(date_from_formatted, date_to_formatted), is_active=True,
                                                                        posting_schedule__health_commodity_balance__location__in=facility_list)

    else:
        query_transactions = HealthCommodityTransactions.objects.filter(is_active=True,
                                                                        posting_schedule__health_commodity_balance__location__in=facility_list)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Posted Transactions.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Disabled Interest')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date Time Posted', 'Health Commodity', 'Quantity available', 'Quantity Consumed', 'Has Patients',
               'Stock Out Days']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = query_transactions.values_list \
        ('date_time_created', 'posting_schedule__health_commodity_balance__health_commodity__health_commodity_name',
         'quantity_available', 'quantity_consumed', 'has_patients', 'stock_out_days')

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response




