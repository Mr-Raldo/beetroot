import json
from channels.generic.websocket import WebsocketConsumer
class BusinessSocketConsumer(WebsocketConsumer):
    def connect(self):
        self.username = "Anonymous"
        self.accept()
        text_data="[Welcome to backend channel %s!]" % self.username
        res = json.dumps({
            "status": 200,
            'topic':'connect webserver',
            "message": text_data
        })
        self.send(res)
        
    def receive(self, *, text_data):
        payload = json.loads(text_data)
        print('json.loads payload', payload)
        print('json.loads profile_id', payload['topic'])

        if payload['topic'] == 'create-booking-order':
            print('data', payload['data'])
            self.username = text_data[5:].strip()
            text_data="[successfull %s]" % payload['topic']
            res = json.dumps({
                "status": 200,
                'topic':'created booking order',
                "message": text_data
            })
            self.send(res)
        else:
            self.send(text_data=payload['topic'] + ": " + 'not successful')

    def disconnect(self, message):
        pass