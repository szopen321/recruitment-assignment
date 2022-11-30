from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from django.test.client import RequestFactory
from Calendar.serializers import UserSerializer


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User


class ConferenceRoomTests(APITestCase):
    def test_create_room(self):
        user = UserFactory.create(username='Alice', password='pass')
        url = reverse('conferenceroom-list')
        context = {'request': RequestFactory().get('/')}
        alice_serializer = UserSerializer(User.objects.get(username='Alice'), context=context)
        data = {
            'name': 'Room of ' + user.username,
            'manager': alice_serializer.data['url'],
            'address': 'Street of ' + user.username,
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201


class CalendarMeetingTest(APITestCase):
    def test_create_view_meeting(self):
        alice_user = UserFactory.create(username='Alice', email='a@a.com')
        bob_user = UserFactory.create(username='Bob', email='b@b.com')
        charlie_user = UserFactory.create(username='Charlie', email='c@c.com')
        url = reverse('meetings-list')
        context = {'request': RequestFactory().get('/')}
        charlie_serializer = UserSerializer(User.objects.get(username='Charlie'), context=context)
        data = {
            "event_name": "test event",
            "meeting_agenda": "test if Bob will be forbidden to see this, while Charlie and Alice won't'",
            "start": "2021-07-07T15:58:00+08:00",
            "end": "2021-07-07T16:58:00+08:00",
            "participant_list": [
                alice_user.email
            ],
            "location": '/rooms/1/'
        }
        location_data = {
            'name': 'Room of ' + charlie_user.username,
            'manager': charlie_serializer.data['url'],
            'address': 'Street of ' + charlie_user.username,
        }
        self.client.force_authenticate(user=bob_user)
        self.client.post('/rooms/', location_data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Bob is neither a participant nor location manager
        response = self.client.get('/meetings/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Charlie is a location manager so can view the meeting
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=charlie_user)
        response = self.client.get('/meetings/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Alice is a participant so she also can view the meeting
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=alice_user)
        response = self.client.get('/meetings/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)