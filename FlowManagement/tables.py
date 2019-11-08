import django_tables2 as tables
from MasterDataManagement import models as master_data_models
from django.utils.safestring import mark_safe
from django.utils.html import escape


class Actions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-xs"><i class="la la-trash"></i></button> ' % (escape(record.id)))


class TransactionActions(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-xs"><i class="la la-trash"></i></button> '
                         '<button id="%s" class="btn_update btn btn-success '
                         'btn-xs"><i class="la la-pencil"></i></button> '% (escape(record.id),escape(record.id)))

class MessagingInboxActions(tables.Column):
        empty_values = list()

        def render(self, value, record):
            return mark_safe('<button id="%s" class="btn_trash_inbox btn btn-secondary'
                             ' btn-xs"><i class="la la-trash"></i></button> '
                             '<button id="%s" class="btn_read btn btn-info '
                             'btn-xs"><i class="la la-eye"></i></button> ' % (escape(record.id),escape(record.id)))

class MessageStatus(tables.Column):

    def render(self):
        return mark_safe('<span ><i class="fa ft-mail red"></i></span>')


class MessagingSentActions(tables.Column):
            empty_values = list()

            def render(self, value, record):
                return mark_safe('<button id="%s" class="btn_trash_sent btn btn-secondary'
                                 ' btn-xs"><i class="la la-trash"></i></button> '
                                 '<button id="%s" class="btn_read btn btn-info '
                                 'btn-xs"><i class="la la-eye"></i></button> ' % (escape(record.id),
                                                                                  escape(record.id)))


class MessagingTrashActions(tables.Column):
                empty_values = list()

                def render(self, value, record):
                    return mark_safe('<button id="%s" class="btn_delete btn btn-secondary'
                                     ' btn-xs"><i class="la la-trash"></i></button> '
                                     '<button id="%s" class="btn_untrash btn btn-warning'
                                     ' btn-xs"><i class="la la-undo"></i></button> '
                                     '<button id="%s" class="btn_read btn btn-info '
                                     'btn-xs"><i class="la la-eye"></i></button> ' % (
                                     escape(record.id), escape(record.id),
                                     escape(record.id)))


class Delete(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_delete btn btn-danger'
                         ' btn-xs"><i class="la la-trash"></i></button> ' % (escape(record.id)))


class Post(tables.Column):
    empty_values = list()

    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn_post btn btn-primary'
                         ' btn-xs"><i class="la icon-paper-plane"></i></button> ' % (escape(record.id)))


class HealthCommodityTransactionTable(tables.Table):
    Action = TransactionActions()
    posting_schedule = tables.Column(verbose_name='Health Commodity')
    date_time_created = tables.DateColumn()
    quantity_available = tables.Column(verbose_name='Stock On Hand')
    location = tables.Column(accessor='posting_schedule.health_commodity_balance.location.location_name')

    class Meta:
        model = master_data_models.HealthCommodityTransactions
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id','date_time_created', 'posting_schedule', 'has_patients', 'quantity_available', 'location')


class ScheduledTransactionTable(tables.Table):
    Action = Post()

    health_commodity_balance = tables.Column(verbose_name='Health Commodity', attrs={
        'td': {
            'class': 'health_commodity_balance'
        }
    })

    location = tables.Column(accessor='health_commodity_balance.location.location_name', verbose_name='Facility Name')

    class Meta:
        model = master_data_models.PostingSchedule
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'health_commodity_balance', 'scheduled_date','location')


class MessageInboxTable(tables.Table):
    Status = MessageStatus()
    Actions = MessagingInboxActions()
    message_body = tables.Column(verbose_name='Message')
    creator = tables.Column(verbose_name='Sender')
    class Meta:
        model = master_data_models.Message
        row_attrs = {
            'data-id': lambda record: record.pk,
            'class': 'message_id'
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'subject', 'message_body', 'creator')


class MessageSentTable(tables.Table):
    Actions = MessagingSentActions()
    message_body = tables.Column(verbose_name='Message')
    class Meta:
        model = master_data_models.Message
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'subject', 'message_body')


class MessageTrashedTable(tables.Table):
    Actions = MessagingTrashActions()
    message_body = tables.Column(verbose_name='Message')
    class Meta:
        model = master_data_models.Message
        row_attrs = {
            'data-id': lambda record: record.pk
        }
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id', 'subject', 'message_body')