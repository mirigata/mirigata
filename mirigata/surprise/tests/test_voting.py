from django.test import TestCase
from surprise import models, forms


class VotingTest(TestCase):

    def test_new_surprise_has_no_votes(self):
        s = models.Surprise.objects.create()
        self.assertEqual(s.points, 0)

    def test_upvote_increases_points(self):
        s = models.Surprise.objects.create()
        cmd = forms.UpvoteCommand(data=dict(
            surprise_id=s.pk,
        ))
        cmd.full_clean()
        cmd.execute()

        s = models.Surprise.objects.get(pk=s.pk)
        self.assertEqual(s.points, 1)

    def test_downvote_decreases_points(self):
        s = models.Surprise.objects.create()
        cmd = forms.DownvoteCommand(data=dict(
            surprise_id=s.pk,
        ))
        cmd.full_clean()
        cmd.execute()

        s = models.Surprise.objects.get(pk=s.pk)
        self.assertEqual(s.points, -1)

