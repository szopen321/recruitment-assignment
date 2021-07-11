from django.db import models
from rest_framework.exceptions import ValidationError
from datetime import timedelta


class CalendarMeeting(models.Model):
    owner = models.ForeignKey('auth.User', related_name='meetings_owned', on_delete=models.CASCADE)
    event_name = models.TextField()
    meeting_agenda = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    participant_list = models.ManyToManyField('auth.User', related_name='meetings_togo')
    location = models.ForeignKey('ConferenceRoom', related_name='meetings_here', blank=True, null=True, default="",
                                 on_delete=models.CASCADE)

    def duration(self):
        value = self.end - self.start
        max_value = timedelta(hours=8)
        if max_value is not None and value > max_value:
            raise ValidationError('Meeting ' + str(self.id) + ' has invalid duration. ' +
                                  'The meeting cannot be longer than 8 hours')
            #
            # I want to give the user option to decide if they want to delete the event
            # or update the event with proper times.
            # Event id is provided for the user for reference.
            # If I wanted to do otherwise I could also delete this invalid event as shown below
            #
            # raise ValidationError(
            #     'The meeting cannot be longer than 8 hours',
            #     self.delete())
            #
        if value <= timedelta(hours=0):
            raise ValidationError(
                'Meeting ' + str(self.id) + ' has invalid duration. ' + 'The event should start before it ends')
        return value


class ConferenceRoom(models.Model):
    manager = models.ForeignKey('auth.User', related_name='rooms_managed', on_delete=models.CASCADE)
    name = models.TextField()
    address = models.TextField()

    def __str__(self):
        return self.name
