# Create your models here.
from django.db import models
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from djmoney.models.fields import MoneyField
from io import BytesIO
from PIL import Image
from django.core.files import File
from .encoders import PrettyJSONEncoder

def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image
User = get_user_model()

class SexChoices(models.TextChoices):
    male = 'male'
    female = 'female'

class ObjectStatus(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    PENDING = "PENDING", _("Pending")
    INACTIVE = "INACTIVE", _("Inactive")
    CANCELLED = "CANCELLED", _("Cancelled")

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    profile_id = models.UUIDField( default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, unique=True)  # Use unique=True for unique email addresses
    email_token = models.CharField(max_length=100, blank=True, null=True)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    neighbourhood = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(choices=SexChoices.choices, default='male', max_length=128)
    status = models.CharField(choices=ObjectStatus.choices, default='Inactive', max_length=128)
    age = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='images/profileImages/', null=True, blank=True)
    immeditiate_needs = models.CharField(max_length=255, null=True, blank=True)
    ideals = models.CharField(max_length=255, null=True, blank=True)
    self_description = models.TextField(null=True, blank=True)
    platform_joining_goals = models.CharField(max_length=255, null=True, blank=True)
    wallet_address = models.CharField(max_length=255, null=True, blank=True)
    online_status = models.BooleanField(null=True, blank=True)
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    xUrl = models.URLField(max_length=255, null=True, blank=True)
    linkedIn_url = models.URLField(max_length=255, null=True, blank=True)
    instagram_url = models.URLField(max_length=255, null=True, blank=True)
    account_type = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    special_skills = models.CharField(max_length=255, null=True, blank=True)
    expected_experience = models.CharField(max_length=255, null=True, blank=True)
    profile_image_url = models.CharField(max_length=255, null=True, blank=True)
    dob = models.CharField(max_length=255, null=True, blank=True)
    community_role = models.CharField(max_length=255, null=True, blank=True)
    business_role = models.CharField(max_length=255, null=True, blank=True)
    trading_industry = models.CharField(max_length=255, null=True, blank=True)
    trading_as = models.CharField(max_length=255, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    portfolio_url = models.URLField(max_length=255, null=True, blank=True)
    is_subscribed = models.BooleanField(null=True, blank=True)
    is_premium_subscribed = models.BooleanField(null=True, blank=True)
    history = HistoricalRecords()
    data = models.JSONField(_("data"), null=True, blank=True, encoder=PrettyJSONEncoder)

    class Meta:
        db_table = "profile"
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
        ordering = ["-first_name"]
        permissions = (("update_statistics", _("Update statistics")),)
    #calling image compression function before saving the data    
    # def save(self, *args, **kwargs):                
    #     profile_image =  compress(self.profile_image)                
    #     self.profile_image = profile_image               
    #     super().save(*args, **kwargs)
    def __str__(self):
        return self.full_name
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.last_name}, {self.first_name}"

        return None

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}"

        return None
    # @mark_safe
    # def pro_image(self, obj):
    #     if self.profile_image.url != None:
    #         return f'<img src="{self.profile_image.url}" height="{self.profile_image.height}" width="{self.profile_image.width}" />'
    #     else:
    #         pass
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
#* Adding model for upvote 


class RequestToEngage(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    requester = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name="requester")
    targeted_profile = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name="targeted_profile")
    
class Subscription(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    expiring_date = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    payment_method = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')
    history = HistoricalRecords()

    def __str__(self):
        return self.business.trading_name

class Wallet(models.Model):
    walletID = models.BigAutoField(primary_key=True, unique=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    deletedDate = models.DateTimeField(null=True, blank=True)
    userID = models.UUIDField(null=True, blank=True)
    walletName = models.CharField(max_length=255, null=True, blank=True)
    walletAddress = models.CharField(max_length=255, null=True, blank=True)
    receiverProfileId = models.BigIntegerField()
    user = models.OneToOneField(Profile, related_name='wallet', on_delete=models.CASCADE)
    currentBalance = MoneyField(
        max_digits=14, decimal_places=2, null=True, blank=True, default_currency=None
    )
    status = models.CharField(
        _("status"), choices=ObjectStatus.choices, null=True, blank=True, max_length=255
    )
    data = models.JSONField(_("data"), null=True, blank=True, encoder=PrettyJSONEncoder)
    objects = HistoricalRecords()

class WalletTransaction(models.Model):
    walletTransactionID = models.BigAutoField(primary_key=True, unique=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    deletedDate = models.DateTimeField(null=True, blank=True)
    walletName = models.CharField(max_length=255, null=True, blank=True)
    transactionNotes = models.TextField(null=True, blank=True)
    transactionStatus = models.CharField(max_length=255, null=True, blank=True)
    smartContractInvoked = models.BooleanField(null=True, blank=True)
    sendingWallet = models.CharField(max_length=255, null=True, blank=True)
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    receivingWallet = models.CharField(max_length=255, null=True, blank=True)
    amount = MoneyField(
        max_digits=14, decimal_places=2, null=True, blank=True, default_currency=None
    )
    blockchainTransactionHash = models.CharField(max_length=255, null=True, blank=True)
    blockHash = models.CharField(max_length=255, null=True, blank=True)
    blockNumber = models.CharField(max_length=255, null=True, blank=True)
    cumulativeGasUsed = models.CharField(max_length=255, null=True, blank=True)
    gasUsed = models.CharField(max_length=255, null=True, blank=True)
    blockchainTransactionMessage = models.TextField(null=True, blank=True)
    contractAddress = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()


