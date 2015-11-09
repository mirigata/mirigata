from django import forms
from django.core.exceptions import PermissionDenied
from django.db import connection, IntegrityError

from . import models


class CreateSurpriseCommand(forms.Form):
    link = forms.URLField()

    def execute(self, user):
        surprise = models.Surprise.objects.create(
            link=self.cleaned_data['link'],
            creator=user,
        )
        models.update_metadata(surprise)

        return surprise


class _VoteCommand(forms.Form):
    increase = 0
    surprise_id = forms.CharField()

    def execute(self, user):
        if user is None:
            raise PermissionDenied()

        pk = self.cleaned_data['surprise_id']

        try:
            models.Vote.objects.create(
                surprise_id=pk,
                user=user,
                amount=self.increase
            )
        except IntegrityError:
            raise PermissionDenied()

        with connection.cursor() as c:
            sql = "update {} set points = points + %s where id = %s".format(
                models.Surprise._meta.db_table,
            )

            c.execute(sql, (self.increase, pk))


class UpvoteCommand(_VoteCommand):
    increase = 1


class DownvoteCommand(_VoteCommand):
    increase = -1
