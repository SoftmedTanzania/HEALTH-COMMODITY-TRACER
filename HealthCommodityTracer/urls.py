
from django.contrib import admin
from django.urls import include, path
from FlowManagement import views as flow_management_views
from API import views as api_views

from background_task.models import Task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('UserManagement.urls')),
    path('api_', include('API.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('health', include('MasterDataManagement.urls')),
    path('new', include('MasterDataManagement.urls')),
    path('update_password', api_views.UpdatePasswordView.as_view(), name='update_password'),
    path('update_google_token', api_views.UpdateGoogleToken.as_view(), name='update_google_token'),
    path('update_read_message_status', api_views.UpdateReadMessageRecipientStatus.as_view(),
         name='update_read_message_status'),
    path('update_parent_message_status', api_views.UpdateParentMessageStatus.as_view(),
         name='update_parent_message_status'),
    path('update_is_trashed_status', api_views.UpdateMessageRecipientsIsTrashed.as_view(),
         name='update_is_trashed_status'),
    path('update_deleted_from_mailbox', api_views.UpdateMessageRecipientsDeletedFromMailbox.as_view(),
         name='update_read_message_status'),
    path('update_quantity_consumed_from_elmis',
         api_views.UpdateHealthCommodityBalanceConsumptionQuantityFromElmis.as_view(),
         name='update_quantity_consumed_from_elmis'),
    path('create_new_message', api_views.ReceivedMessageView.as_view(), name='create_new_message'),
    path('save_transaction', include('FlowManagement.urls')),
    path('save_commodity', include('MasterDataManagement.urls')),
    path('update', include('MasterDataManagement.urls')),
    path('get_category', include('MasterDataManagement.urls')),
    path('post', include('FlowManagement.urls')),
    path('send', include('FlowManagement.urls')),
    path('reporting', include('Reporting.urls')),
    path('fcm', include('fcm.urls')),

]

flow_management_views.update_consumption_data_from_elmis(repeat=2, repeat_until=None)
