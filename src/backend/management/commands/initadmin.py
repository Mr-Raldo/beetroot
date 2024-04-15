import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    print('Command:: Admin account initializing')
    def handle(self, *args, **options):
        DJANGO_DB_NAME = os.environ.get('DJANGO_DB_NAME', "default")
        DJANGO_SU_NAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        print('Command:: DJANGO_SU_NAME', DJANGO_SU_NAME)
        print('Command:: DJANGO_SU_EMAIL', DJANGO_SU_EMAIL)
        print('Command:: DJANGO_SU_PASSWORD', DJANGO_SU_PASSWORD)
        print('Command:: Admin account initializing')
        print('Command:: User.objects.count()', User.objects.count())
        print('Command:: User.objects.count()', User.objects.all())
        
        if User.objects.count() == 0:
            superuser = User.objects.create_superuser(
                username=DJANGO_SU_NAME,
                email=DJANGO_SU_EMAIL,
                password=DJANGO_SU_PASSWORD)
            superuser.save()
            if superuser:
                print('Admin account initialized')
            else:
                print('Admin account not initialized')
        else:
            try:
                user = User.objects.get(username=DJANGO_SU_NAME)
                print('Command:: user already exists', user)
            except User.DoesNotExist:
                print('Command:: Does Not Exist')
                superuser = User.objects.create_superuser(
                    username=DJANGO_SU_NAME,
                    email=DJANGO_SU_EMAIL,
                    password=DJANGO_SU_PASSWORD)
                superuser.save()
                if superuser:
                    print('Admin account initialized')
                else:
                    print('Admin account not initialized')

 




        # if Account.objects.count() == 0:
        #     for user in settings.ADMINS:
        #         username = user[0].replace(' ', '')
        #         email = user[1]
        #         password = 'admin'
        #         print('Creating account for %s (%s)' % (username, email))
        #         admin = Account.objects.create_superuser(email=email, username=username, password=password)
        #         admin.is_active = True
        #         admin.is_admin = True
        #         admin.save()
        # else:
        #     print('Admin accounts can only be initialized if no Accounts exist')