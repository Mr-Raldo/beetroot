import time
from datetime import timedelta
from uuid import uuid4
from firebase_admin import firestore, initialize_app, messaging
from uuid import uuid4
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework.response import Response
from rest_framework import status

__all__ = ['add_profile_to_firebase', 'send_to_firebase', 'update_firebase_snapshot']

initialize_app()

@api_view(['GET'])
def profile_to_firebase(request):
    profiles = Profile.objects.all()
    total_spend_time = 0

    for profile in profiles:
        serialized_data = ProfileSerializer(profile).data
        spend_time = add_profile_to_firebase(serialized_data)
        total_spend_time += spend_time

    return JsonResponse({'message': 'Profiles added to Firebase successfully.', 'total_spend_time': str(total_spend_time)})


def add_profile_to_firebase(profile_data):
    db = firestore.client()
    start = time.time()
    doc_ref = db.collection('profiles').document()
    doc_ref.set(profile_data)
    end = time.time()
    spend_time = end - start
    return spend_time

def add_exhibit_to_firebase(exhibit_data):
    db = firestore.client()
    start = time.time()
    doc_ref = db.collection('exhibits').document(str(uuid4()))
    doc_ref.set(exhibit_data)
    end = time.time()
    spend_time = end - start
    return spend_time


def send_to_firebase(raw_notification):
    db = firestore.client()
    start = time.time()
    db.collection('notifications').document(str(uuid4())).create(raw_notification)
    end = time.time()
    spend_time = timedelta(seconds=end - start)
    return spend_time


def update_firebase_snapshot(snapshot_id):
    start = time.time()
    db = firestore.client()
    db.collection('notifications').document(snapshot_id).update(
        {'is_read': True}
    )
    end = time.time()
    spend_time = timedelta(seconds=end - start)
    return 

@api_view(['POST'])
def sendMessage(request):
    data = request.data
    token = data.get('token')
    notification = data.get('notification')
    print('token')
    print(token)
    # Create a message to send
    message = messaging.Message(
        notification=messaging.Notification(
            title=notification.get('sender'),
            body=notification.get('body')
        ),
        token=token
    )

    # Send the message
    response = messaging.send(message)
    print('Successfully sent message:', response)   
     
    return Response(response, status=status.HTTP_200_OK)