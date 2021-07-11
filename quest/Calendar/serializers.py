from rest_framework import serializers
from Calendar.models import CalendarMeeting, ConferenceRoom
from django.contrib.auth.models import User
from django.utils import timezone


class DateTimeWithTZ(serializers.DateTimeField):

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeWithTZ, self).to_representation(value)


class ConferenceRoomSerializer(serializers.HyperlinkedModelSerializer):
    meetings_here = serializers.HyperlinkedRelatedField(many=True, view_name='meetings-detail', read_only=True)

    class Meta:
        model = ConferenceRoom
        fields = ['name', 'manager', 'id', 'address', 'meetings_here']


class CalendarMeetingReadSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    participant_list = serializers.SlugRelatedField(
        many=True,
        slug_field='email',
        queryset=User.objects.all()
     )
    start = DateTimeWithTZ()
    end = DateTimeWithTZ()
    duration = serializers.DurationField(read_only=True)
    location = ConferenceRoomSerializer()

    class Meta:
        model = CalendarMeeting
        fields = ['id', 'owner', 'event_name', 'meeting_agenda', 'start', 'end', 'duration', 'participant_list',
                  'location']


class CalendarMeetingWriteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    participant_list = serializers.SlugRelatedField(
        many=True,
        slug_field='email',
        queryset=User.objects.all()
     )
    start = DateTimeWithTZ()
    end = DateTimeWithTZ()
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = CalendarMeeting
        fields = ['id', 'owner', 'event_name', 'meeting_agenda', 'start', 'end', 'duration', 'participant_list',
                  'location']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    meetings_owned = serializers.HyperlinkedRelatedField(many=True, view_name='meetings-detail', read_only=True)
    meetings_togo = serializers.HyperlinkedRelatedField(many=True, view_name='meetings-detail', read_only=True)
    rooms_managed = serializers.HyperlinkedRelatedField(many=True, view_name='conferenceroom-detail', queryset=User.objects.all())

    class Meta:
        model = User
        fields = ['email', 'url', 'id', 'username', 'meetings_owned', 'meetings_togo', 'rooms_managed']
