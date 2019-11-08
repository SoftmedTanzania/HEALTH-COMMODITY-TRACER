from django.contrib.auth.models import User
from django.db import models
from MasterDataManagement import models as master_data_models
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Profile(models.Model):
    def __str__(self):
        return '%s' % self.user.first_name

    Female = 'Female'
    Male = 'Male'

    GENDER_TYPE_CHOICES = (
        (Female, 'Female'),
        (Male, 'Male')
    )

    date_time_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, choices=GENDER_TYPE_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    location = TreeForeignKey(master_data_models.Location, on_delete=models.SET_NULL, null=True)
    reg_id = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'HCT_UserProfiles'


class TokenModel(models.Model):
    key = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)

    class Meta:
        db_table = 'HCT_UserTokens'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()




