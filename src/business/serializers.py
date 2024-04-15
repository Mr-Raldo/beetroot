from rest_framework import serializers
from .models import Business,ProductImage,Product, Service,ServiceImage


class BusinessSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField('get_logo_url')
    main_banner_image_url = serializers.SerializerMethodField('get_main_banner_image_url')
    services = serializers.SerializerMethodField('get_services')
    class Meta:
        model = Business
        fields = ('id','entreprenuer',
                  'created_date','updated_date',
                  'deleted_date','wallet_address',
                  'online_status','email','phone',
                  'neighbourhood','city','country',
                  'street_address','portfolio_url',
                  'facebook_url','x_url','linkedin_url',
                  'instagram_url','admin_user_id',
                  'account_type','specialization',
                  'motto','service_type','trading_name',
                  'business_description','short_term_goals',
                  'long_term_goals','business_stage',
                  'business_registration_number',
                  'target_market_countries',
                  'target_market_cities','short_term_goal',
                  'long_term_goal','trade_sector',
                  'search_term',
                  'main_banner_image_url',
                  'logo_url',
                  'is_subscribed',
                  'is_premium_subscribed',
                  'services' )

    # @staticmethod
    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        else:
            return ''
        
    # @staticmethod
    def get_main_banner_image_url(self, obj):
        if obj.main_banner_image:
            return obj.main_banner_image.url
        else:
            return ''
            # @staticmethod
    def get_services(self, obj):
        services = Service.objects.filter(business=obj)
        serializer = ServiceSerializer(services, many=True)
        return serializer.data
        
class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ('image',)


class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = ('id', 'created_date', 'updated_date','deleted_date', 'name', 'category', 'description','price','is_trending','trade_status','entreprenuer','business','images')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
