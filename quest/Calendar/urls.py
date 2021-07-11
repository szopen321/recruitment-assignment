from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Calendar import views

router = DefaultRouter()
router.register(r'meetings', views.CalendarMeetingViewSet, basename='meetings')
router.register(r'rooms', views.ConferenceRoomViewSet, basename='conferenceroom')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
