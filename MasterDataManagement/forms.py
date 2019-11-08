from django import forms
from django.contrib.auth.models import User
from .models import HealthCommodity, HealthCommoditiesCategory, Unit, HealthCommodityBalance,\
    PostingFrequency, Location


class HealthCommodityForm(forms.ModelForm):
    health_commodity_category = forms.ModelChoiceField(queryset=HealthCommoditiesCategory.objects.filter(is_active=True),
                                   to_field_name='id',
                                   empty_label="Select Category")

    unit = forms.ModelChoiceField(
        queryset=Unit.objects.filter(is_active=True),
        to_field_name='id',
        empty_label="Select Unit")

    posting_frequency = forms.ModelChoiceField(
        queryset=PostingFrequency.objects.filter(is_active=True),
        to_field_name='id',
        empty_label="Select Frequency")

    class Meta:
        model = HealthCommodity
        fields = ('health_commodity_name', "elims_product_id", 'description', 'health_commodity_category', 'unit', 'posting_frequency',
                  'track_number_of_patients', 'track_wastage', 'track_quantity_expired')


class HealthCommodityCategoryForm(forms.ModelForm):
    class Meta:
        model = HealthCommoditiesCategory
        fields = ('health_commodity_category_name','description')

        widgets = {
            'health_commodity_category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('abbreviation', 'unit_description')

        widgets = {
            'abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('id','elims_facility_id', 'location_name', 'location_type', 'facility_type', 'parent')


class PostFrequencyForm(forms.ModelForm):
    class Meta:
        model = PostingFrequency
        fields = ('frequency_description', "number_of_days")

        widgets = {
            'frequency_description': forms.TextInput(attrs={'class': 'form-control'}),
            "number_of_days": forms.TextInput(attrs={'class': 'form-control'}),
        }


class HealthCommodityBalanceForm(forms.ModelForm):
    class Meta:
        model = HealthCommodityBalance
        fields = ('health_commodity', 'quantity_available', 'quantity_consumed',
                  'quantity_wasted','quantity_expired', 'has_clients', 'number_of_clients')


class UploadFileForm(forms.Form):
    file = forms.FileField()


class eLIMSLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    model = User
    widgets = {
        'password': forms.PasswordInput(),
    }


class LocationTreeForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('parent',)
        labels = {
            'parent': 'Location',
        }