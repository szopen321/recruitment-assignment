from Calendar.models import CalendarMeeting, ConferenceRoom
from Calendar.serializers import CalendarMeetingReadSerializer, CalendarMeetingWriteSerializer, ConferenceRoomSerializer, UserSerializer
from django.contrib.auth.models import User
from Calendar.permissions import IsOwnerOrReadOnly, IsParticipantOrRoomManager
from rest_framework import viewsets
from rest_framework import permissions
from django.db.models import Q


class CalendarMeetingViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarMeetingReadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, IsParticipantOrRoomManager]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial-update']:
            return CalendarMeetingWriteSerializer
        return CalendarMeetingReadSerializer

    def get_queryset(self):

        queryset = CalendarMeeting.objects.all()
        if self.action == 'list':
            queryset = queryset.filter(Q(location__manager=self.request.user) | Q(participant_list=self.request.user))
        day = self.request.query_params.get('day')
        location_id = self.request.query_params.get('location_id')
        query = self.request.query_params.get('query')
        if day is not None:
            queryset = queryset.filter(start__date=day)
        if location_id is not None and self.object.location is not None:
            queryset = queryset.filter(location__id=location_id)
        if query is not None:
            queryset = queryset.filter(Q(event_name=query) | Q(meeting_agenda=query))

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ConferenceRoomViewSet(viewsets.ModelViewSet):
    queryset = ConferenceRoom.objects.all()
    serializer_class = ConferenceRoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
