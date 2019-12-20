from django import forms
from MasterDataManagement import models as master_data_models


class PostCommodityForm(forms.ModelForm):
    # health_commodity_balance = forms.ModelChoiceField(queryset=master_data_models.HealthCommodityBalance.
    #                                           objects.all(),
    #                                to_field_name='health_commodity',
    #                                empty_label="Select Commodity")

    class Meta:
        model = master_data_models.HealthCommodityTransactions
        fields = ('posting_schedule','quantity_available','quantity_consumed', 'has_patients',
                  'stock_out_days', 'number_of_clients', 'quantity_expired', 'quantity_wasted')
        widgets = {
            'number_of_patients': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_consumed': forms.TextInput(attrs={'readonly':'readonly'}),
            'posting_schedule': forms.TextInput(attrs={'readonly': 'readonly'})
        }
        labels = {
            'quantity_available':'Stock on Hand',
            'quantity_consumed': 'Average Monthly Consumption',
            'has_patients': 'Does this commodity have clients? (Tick if yes)',
        }


class ComposeMessageForm(forms.ModelForm):

    class Meta:
        model = master_data_models.Message
        fields = ('subject', 'message_body')


class MessageRecipientsForm(forms.ModelForm):

    class Meta:
        model = master_data_models.MessageRecipient
        fields = ('recipient', 'location', 'message')
