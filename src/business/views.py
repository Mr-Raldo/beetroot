from django.views.generic import TemplateView
from web_project import TemplateLayout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from akyc.models import Profile
from akyc.serializers import ProfileSerializer
import json
import uuid

from .models import (
    Business,
    ProductImage,
    Product,
    Service,
    ServiceImage,
)
from .serializers import (
    BusinessSerializer,
    ProductImageSerializer,
    ProductSerializer,

    ServiceSerializer,
    ServiceImageSerializer,

)


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to ecommerce/urls.py file for more pages.
"""


class businessView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context

@api_view(['GET', 'POST'])
def business_list(request, format=None):
    if request.method == 'GET':
        print('request data',request.data)
        providers = Business.objects.all()
        serializer = BusinessSerializer(providers, many=True)
        return Response({'data': json.dumps(serializer.data)}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        print('Post method request.data',request.data )
        service_item_str = request.POST.get('service-item', '')
            # Convert the JSON string to a dictionary
        business_profile = json.loads(service_item_str)
        print('business_profile')
        
        print('file', request.FILES.get('file'))
        print('logo', request.FILES.get('logo'))
        print('banner', request.FILES.get('banner'))
        entreprenuer = Profile.objects.get(profile_id=business_profile['adminUserID'])
        token = str(uuid.uuid4())
        business, created = Business.objects.get_or_create(
            entreprenuer = entreprenuer,
            wallet_address = token,
            city = business_profile['operationsCity'],
            country = business_profile['operationsCountry'],
            admin_user_id = business_profile['adminUserID'],
            account_type = 'provider',
            specialization = business_profile['specialization'],
            motto = business_profile['motto'],
            service_type = business_profile['specialization'],
            trading_name = business_profile['tradingName'],
            business_description = business_profile['businessDescription'],
            short_term_goals = business_profile['adminUserID'],
            long_term_goals = business_profile['adminUserID'],
            business_stage = business_profile['adminUserID'],
            business_registration_number = business_profile['gvtIssuedBusinessRegistraID'],
            target_market_countries = business_profile['targetMarketCountries'],
            target_market_cities = business_profile['targetMarketCities'],
            trade_sector = business_profile['tradeSector'],
            search_term = business_profile['tradeSector'] + business_profile['specialization'] + business_profile['tradingName'],
            main_banner_image =  request.FILES.get('banner'),
            logo =  request.FILES.get('logo')
         )
        print(business, created)
        if created:
            new_business = Business.objects.get(pk=business.id)
            serializer = BusinessSerializer(new_business)
            print('json.dumps(new_business)', json.dumps(serializer.data))
            return Response(json.dumps(serializer.data), status=status.HTTP_201_CREATED)

    return Response({'message': 'Invalid HTTP method'})

@api_view(['GET'])
def get_entreprenuer_businesses(request, profile_id, format=None):
    try:
        businesses = Business.objects.filter(admin_user_id=profile_id)
    except Business.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = BusinessSerializer(businesses, many=True )
    return Response({'data':json.dumps(serializer.data)}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def services(request, format=None):
    if request.method == 'GET':
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response({'services': json.dumps(serializer.data)  }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        service_item_str = request.POST.get('service-item', '')
        business_profile = json.loads(service_item_str)

        business = None
        entreprenuer = None
        new_service = None
        if business_profile['providerAccountType'] == 'business':
            business =  Business.objects.get(pk=business_profile['providerID'])
        else:
            entreprenuer = Profile.objects.get(profile_id=business_profile['providerID'])

        if business_profile['providerAccountType'] == 'business':
            new_service, created = Service.objects.get_or_create(
                        category = business_profile['category'],
                        trade_status = business_profile['tradeStatus'],
                        is_trending = False,
                        description = business_profile['description'],
                        name = business_profile['name'],
                        price = business_profile['price'],
                        business = business
                        )
            print('business new_service created', created)
 
        else:
            new_service, created = Service.objects.get_or_create(
                        category = business_profile['category'],
                        trade_status = business_profile['tradeStatus'],
                        is_trending = False,
                        description = business_profile['description'],
                        name = business_profile['name'],
                        price = business_profile['price'],
                        entreprenuer = entreprenuer 
                )
            print('entreprenuer new_service created', created)
        if new_service:
            images = request.FILES.getlist('file')  # Use getlist to handle multiple files
            for img in images:
                imge = ServiceImage.objects.create(
                    service=new_service,
                    image=img
                )
            service_instance = Service.objects.prefetch_related('images').get(id=new_service.id)
            # Serialize the Service object with nested ServiceImage serialization
            serializer = ServiceSerializer(service_instance)

            print('service_serializer', serializer.data)

            return Response({'data':json.dumps(serializer.data)}, status=status.HTTP_201_CREATED)

        return Response({'message': 'Invalid HTTP method'})





    
# entreprenuers

@api_view(['GET', 'POST'])
def entreprenuers(request, format=None):
    if request.method == 'GET':
        entreprenuers = Profile.objects.filter(account_type='provider')
        serializer = ProfileSerializer(entreprenuers, many=True)
        return Response({'data': json.dumps(serializer.data)  }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        print('Post method')
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('serializer.is NOT valid')

    return Response({'message': 'Invalid HTTP method'})
@api_view(['GET', 'PUT', 'DELETE'])
def entreprenuer(request, profile_id, format=None):
    try:
        print('profile_id', profile_id)
        profile = Profile.objects.get(pk=profile_id)
    except Profile.DoesNotExist:
        print('Profile.DoesNotExist', profile_id)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        serializer = ProfileSerializer(profile)
        print('entreprenuer', serializer.data)
        return Response({'entreprenuer': json.dumps(serializer.data)})


    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def business_detail(request, id, format=None):
    try:
        provider = Business.objects.get(pk=id)
    except Business.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BusinessSerializer(provider)
        return Response({'provider': serializer.data})

    elif request.method == 'PUT':
        serializer = BusinessSerializer(provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Service Booking Views
# Service Views
@api_view(['GET', 'POST'])
def business_services(request, business_id, format=None):
    if request.method == 'GET':
        if business_id:
            print('business_id', business_id)
            business = Business.objects.get(pk=business_id)
            services = business.services.all()  # Assuming a reverse relation in Entrepreneur model
            serializer = ServiceSerializer(services, many=True, context={'request': request})
            return Response({'services': json.dumps(serializer.data) }, status=status.HTTP_200_OK)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response({'services': json.dumps(serializer.data)  }, status=status.HTTP_200_OK)
@api_view(['GET', 'POST'])
def entreprenuer_services(request, profile_id, format=None):
    if request.method == 'GET':
        if profile_id:
            print('profile_id', profile_id)
            entrepreneur = Profile.objects.get(profile_id=profile_id)
            services = entrepreneur.services.all()  # Assuming a reverse relation in Entrepreneur model
            serializer = ServiceSerializer(services, many=True, context={'request': request})
            return Response({'services': json.dumps(serializer.data) }, status=status.HTTP_200_OK)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response({'services': json.dumps(serializer.data)  }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def services_list(request, phone, format=None):
    if request.method == 'GET':
        if phone:
            print('phone', phone)
            entrepreneur = Profile.objects.get(phone=phone)
            services = entrepreneur.services.all()  # Assuming a reverse relation in Entrepreneur model
            serializer = ServiceSerializer(services, many=True, context={'request': request})
            return Response({'services': json.dumps(serializer.data) }, status=status.HTTP_200_OK)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response({'services': json.dumps(serializer.data)  }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        print('request.data', request.data)
        # service_data_str = request.POST.get('service-item', '')
        service_data = request.data.get('service-item', {})
        images = request.FILES.getlist('file')  # Use getlist to handle multiple files
        print('service_data .data', service_data)
        service_data = json.loads(service_data)

        serializer = ServiceSerializer(data=service_data)
        print('serializer', serializer.is_valid())

        if serializer.is_valid():
            if service_data['business_id']:
                business = Business.objects.get(pk=service_data['business_id'])
                Service.objects.create(
                    business = business,
                    category = service_data['category'],
                    trade_status = service_data['trade_status'],
                    is_trending = service_data['is_trending'],
                    description = service_data['description'],
                    name = service_data['name'],
                    price = service_data['price'],
                    )
            if service_data['entreprenuer_id']:
                print("service_data['entreprenuer_id']", service_data['entreprenuer_id'])

                entreprenuer = Profile.objects.get(pk=service_data['entreprenuer_id'])
                print("entreprenuer", entreprenuer)


                new_service = Service.objects.create(
                    entreprenuer=entreprenuer,
                    category=service_data.get('category'),
                    trade_status=service_data.get('trade_status'),
                    is_trending=service_data.get('is_trending'),
                    description=service_data.get('description'),
                    name=service_data.get('name'),
                    price=service_data.get('price'),
                )
                print("new_service", new_service)
                if new_service:
                    images = request.FILES.getlist('file')  # Use getlist to handle multiple files

                    for img in images:
                        imge = ServiceImage.objects.create(
                            service=new_service,
                            image=img
                        )
                    service_instance = Service.objects.prefetch_related('images').get(id=new_service.id)
                    # Serialize the Service object with nested ServiceImage serialization
                    serializer = ServiceSerializer(service_instance)

                    print('service_serializer', serializer.data)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'message': 'Invalid HTTP method'})

@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, id, format=None):
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response({'service': serializer.data})

    elif request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Service Image Views
@api_view(['GET', 'POST'])
def service_images_list(request, format=None):
    if request.method == 'GET':
        service_images = ServiceImage.objects.all()
        serializer = ServiceImageSerializer(service_images, many=True)
        return Response({'service_images': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ServiceImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'message': 'Invalid HTTP method'})

@api_view(['GET', 'PUT', 'DELETE'])
def service_image_detail(request, id, format=None):
    try:
        service_image = ServiceImage.objects.get(pk=id)
    except ServiceImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceImageSerializer(service_image)
        return Response({'service_image': serializer.data})

    elif request.method == 'PUT':
        serializer = ServiceImageSerializer(service_image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        service_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Product Views
@api_view(['GET', 'POST'])
def products_list(request, format=None):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'message': 'Invalid HTTP method'})

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id, format=None):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response({'product': serializer.data})

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Product Image Views
@api_view(['GET', 'POST'])
def product_images_list(request, format=None):
    if request.method == 'GET':
        product_images = ProductImage.objects.all()
        serializer = ProductImageSerializer(product_images, many=True)
        return Response({'product_images': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'message': 'Invalid HTTP method'})

@api_view(['GET', 'PUT', 'DELETE'])
def product_image_detail(request, id, format=None):
    try:
        product_image = ProductImage.objects.get(pk=id)
    except ProductImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductImageSerializer(product_image)
        return Response({'product_image': serializer.data})

    elif request.method == 'PUT':
        serializer = ProductImageSerializer(product_image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
