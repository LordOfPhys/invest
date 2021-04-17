from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    first_name = models.CharField(max_length=30, default='name')
    last_name = models.CharField(max_length=30, default='name')
    email = models.CharField(max_length=100, default='email')
    image = models.ImageField(upload_to='people_images/')

    def __str__(self):
        return self.email

    def get_user(self):
        return self.user

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name
        self.save()

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name
        self.save()

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email
        self.save()

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image
        self.save()

class TeamProject(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    label = models.CharField(max_length=500, default='label')
    money_amount = models.IntegerField(default='0')
    location = models.CharField(max_length=500, default='location')
    description = models.CharField(max_length=20000, default='description')
    fileproject = models.FileField(upload_to='uploads/')
    actual = models.BooleanField(default=True)
    visitors = models.IntegerField(default='0')
    date = models.DateField(default='01-01-2020')
    item_id = models.IntegerField(default='0', unique=True)

    def get_item_id(self):
        return self.item_id

    def set_item_id(self, item_id):
        self.item_id = item_id
        self.save()

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date
        self.save()

    def get_user_profile(self):
        return self.userprofile

    def get_actual(self):
        return self.actual

    def set_actual(self, actual):
        self.actual = actual
        self.save()

    def get_visitors(self, actual):
        return self.visitors

    def set_visitors(self):
        self.visitors += 1
        self.save()

    def get_label(self):
        return self.label

    def get_money_amount(self):
        return self.money_amount

    def get_location(self):
        return self.location

    def get_description(self):
        return self.description

    def get_file(self):
        return self.fileproject

    def __str__(self):
        return self.label

class InvestProject(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    label = models.CharField(max_length=500, default='label')
    money_amount = models.IntegerField(default='0')
    location = models.CharField(max_length=500, default='location')
    description = models.CharField(max_length=20000, default='description')
    fileproject = models.FileField(upload_to='uploads/')
    actual = models.BooleanField(default=True)
    visitors = models.IntegerField(default='0')
    date = models.DateField(default='01-01-2020')
    item_id = models.IntegerField(default='0', unique=True)

    def get_item_id(self):
        return self.item_id

    def set_item_id(self, item_id):
        self.item_id = item_id
        self.save()
    
    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date
        self.save()

    def get_user_profile(self):
        return self.userprofile
    
    def get_actual(self):
        return self.actual

    def set_actual(self, actual):
        self.actual = actual
        self.save()

    def get_visitors(self, actual):
        return self.visitors

    def set_visitors(self):
        self.visitors += 1
        self.save()

    def get_label(self):
        return self.label

    def get_money_amount(self):
        return self.money_amount

    def get_location(self):
        return self.location

    def get_description(self):
        return self.description

    def get_file(self):
        return self.fileproject

    def __str__(self):
        return self.label
