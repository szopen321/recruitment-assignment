from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsParticipantOrRoomManager(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user in obj.participant_list.all():
            return True
        elif obj.location:
            if request.user == obj.location.manager:
                return True
