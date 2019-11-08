from django.urls import path
from FlowManagement import views


urlpatterns = [
path('view_transactions', views.view_health_commodity_transactions,name='view_transactions'),
path('get_scheduled_transaction_page', views.get_scheduled_transaction_page, name='get_scheduled_transaction_page'),
path('get_post_commodity_page/<int:item_pk>/', views.get_post_commodity_page, name='get_post_commodity_page'),
path('get_repost_schedule_page', views.get_repost_schedules_page, name='get_repost_schedule_page'),
path('save_posted_transaction', views.save_posted_transaction, name='save_posted_transaction'),
path('facility_ranking', views.get_facility_by_post, name='facility_ranking'),
path('get_messaging_page', views.get_messaging_page, name='get_messaging_page'),
path('get_message_thread_page/<int:item_pk>', views.get_message_thread_page, name='get_message_thread_page'),
path('send_user_a_push_notification', views.send_user_a_push_notification,
     name='send_user_a_push_notification'),
path('send_thread_message', views.send_thread_message, name='send_thread_message'),
path('trash_email', views.trash_email, name='trash_email'),
path('trash_inbox_message', views.trash_inbox_message, name='trash_inbox_message'),
path('untrash_email', views.untrash_email, name='untrash_email'),
path('delete_from_mail_box', views.delete_from_mail_box, name='delete_from_mail_box'),
path('load_inbox', views.load_inbox, name='load_inbox'),
path('load_sent_items', views.load_sent_items, name='load_sent_items'),
path('load_trash_items', views.load_trash_items, name='load_trash_items'),
path('get_jasper_server_instance', views.get_jasper_server_instance, name='get_jasper_server_instance'),

]