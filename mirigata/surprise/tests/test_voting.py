from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.utils.functional import SimpleLazyObject

from surprise import models, forms
from django.contrib.auth import models as auth


class VotingTest(TestCase):

    def setUp(self):
        self.user = auth.User.objects.create_user(username='xyz', password='xyz')
        self.other_user = auth.User.objects.create_user(username='qqq', password='qqq')

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

    def test_different_users_can_vote_for_same_surprise(self):
        self.upvote_command.execute(user=self.user)
        self.upvote_command.execute(user=self.other_user)

        s = models.Surprise.objects.get(pk=self.surprise.pk)
        self.assertEquals(s.votes.count(), 2)

    def test_retrieve_votes_for_user(self):
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNone(vote)

        self.upvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNotNone(vote)

        vote = models.Vote.objects.get_vote_for(user=self.other_user, surprise_id=self.surprise.pk)
        self.assertIsNone(vote)

    def test_after_upvote_upvoting_again_will_remove_vote(self):
        self.upvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNotNone(vote)

        self.upvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNone(vote)

        s = models.Surprise.objects.get(pk=self.surprise.pk)
        self.assertEquals(s.points, 0)

    def test_after_upvote_downvoting_again_will_remove_vote(self):
        self.upvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNotNone(vote)

        self.downvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNone(vote)

        s = models.Surprise.objects.get(pk=self.surprise.pk)
        self.assertEquals(s.points, 0)

    def test_after_downvote_upvoting_will_remove_vote(self):
        self.downvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNotNone(vote)

        self.upvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNone(vote)

        s = models.Surprise.objects.get(pk=self.surprise.pk)
        self.assertEquals(s.points, 0)

    def test_after_downvote_downvoting_will_remove_vote(self):
        self.downvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNotNone(vote)

        self.downvote_command.execute(user=self.user)
        vote = models.Vote.objects.get_vote_for(user=self.user, surprise_id=self.surprise.pk)
        self.assertIsNone(vote)

        s = models.Surprise.objects.get(pk=self.surprise.pk)
        self.assertEquals(s.points, 0)

    def test_dont_raise_error_when_user_is_not_present(self):
        vote = models.Vote.objects.get_vote_for(user=None, surprise_id=self.surprise.pk)
        self.assertIsNone(vote)


class VoteModelTest(TestCase):

    def test_upvote(self):
        vote = models.Vote(amount=1)
        self.assertTrue(vote.is_upvote())
        self.assertFalse(vote.is_downvote())

    def test_downvote(self):
        vote = models.Vote(amount=-1)
        self.assertTrue(vote.is_downvote())
        self.assertFalse(vote.is_upvote())

