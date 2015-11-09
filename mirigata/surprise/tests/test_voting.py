from django.core.exceptions import PermissionDenied
from django.test import TestCase
from surprise import models, forms
from django.contrib.auth import models as auth


class VotingTest(TestCase):

    def setUp(self):
        self.user = auth.User.objects.create_user(username='xyz', password='xyz')

        self.surprise = models.Surprise.objects.create()
        self.upvote_command = forms.UpvoteCommand(data=dict(
            surprise_id=self.surprise.pk,
        ))
        self.upvote_command.full_clean()

        self.downvote_command = forms.DownvoteCommand(data=dict(
            surprise_id=self.surprise.pk,
        ))
        self.downvote_command.full_clean()

    def test_new_surprise_has_no_votes(self):
        self.assertEqual(self.surprise.points, 0)

    def test_upvote_increases_points(self):
        self.upvote_command.execute(user=self.user)

        s = models.Surprise.objects.get(pk=self.surprise.pk)
        self.assertEqual(s.points, 1)

    def test_downvote_decreases_points(self):
        self.downvote_command.execute(user=self.user)

        s = models.Surprise.objects.get(pk=self.surprise.pk)
        self.assertEqual(s.points, -1)

    def test_upvote_requires_user(self):
        self.assertRaises(PermissionDenied, self.upvote_command.execute, user=None)

    def test_upvoting_can_happen_only_once(self):
        self.upvote_command.execute(user=self.user)
        self.assertRaises(PermissionDenied, self.upvote_command.execute, user=self.user)


