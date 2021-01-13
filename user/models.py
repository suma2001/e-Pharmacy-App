from django.contrib.auth.models import User, AbstractBaseUser
from django.db import models
from cart.models import Cart
from django.db.models.signals import post_save
from django.dispatch import receiver

USER_TYPE = (
    (1, 'users'),
    (2, 'shops')
)

class History(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ordered_date = models.DateTimeField()
    ordered_items = models.ManyToManyField("cart.Cart")

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE, default=1)
    cart_items=models.ManyToManyField(Cart)
    signup_confirmation = models.BooleanField(default=False)
    address = models.CharField(max_length=256, default=True)
    history = models.ManyToManyField(History)

class Shop(models.Model):
    username = models.CharField(max_length=50, default=True)
    set_password = models.CharField(max_length=50, default=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE, default=2)
    shop_name = models.CharField(max_length=256, default=True)
    shop_registration_no = models.CharField(max_length=256, default=True)
    address = models.CharField(max_length=256, default=True)
    latitude = models.FloatField(max_length=50, default=0)
    longitude = models.FloatField(max_length=50, default=0)
    distance = models.FloatField(max_length=50, default=0)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.shop_name

@receiver(post_save,sender=User)
def update_profile_signal(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()






