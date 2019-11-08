from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('profiles', views.ProfileView)
router.register('user_profile', views.UserProfileView)
router.register('health_commodity', views.HealthCommodityView)
router.register('health_commodity_category', views.HealthCommodityCategoryView)
router.register('health_commodity_mapping', views.HealthCommodityBalanceView)
router.register('unit', views.UnitView)
router.register('facility_types', views.FacilityTypeView)
router.register('locations', views.LocationsView)
router.register('health_commodity_transactions', views.HealthCommodityTransactionView)
router.register('posting_frequency', views.PostingFrequencyView)
router.register('posting_schedule', views.PostingScheduleView)
router.register('messages', views.MessageView)
router.register('message_recipients', views.MessageRecipientsView)

urlpatterns = [
    path('', include(router.urls)),
    path('update_password', views.UpdatePasswordView.as_view(), name='update_password'),
    path('login', include('rest_auth.urls'), name='apiLogin'),
]