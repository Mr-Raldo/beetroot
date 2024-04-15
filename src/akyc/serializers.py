from rest_framework import serializers
from .models import Profile, Subscription, Wallet, WalletTransaction
from business.models import Business,ProductImage,Product, Service,ServiceImage
from business.serializers import (
    BusinessSerializer,
    ProductImageSerializer,
    ProductSerializer,
    ServiceSerializer,
    ServiceImageSerializer,

)
class ProfileSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField('get_services')
    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ['profile_image', 'age']
    # @staticmetho
    def get_services(self, obj):
        services = Service.objects.filter(entreprenuer=obj)
        serializer = ServiceSerializer(services, many=True)
        return serializer.data
    
    
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'
