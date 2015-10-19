from django.test import TestCase

from surprise import models


class WikipediaMetadataTestCase(TestCase):
    def setUp(self):
        self.metadata = {
            "author_name": None,
            "canonical_url": "https://en.wikipedia.org/wiki/Main_Page",
            "description": None,
            "og_description": None,
            "og_image": None,
            "og_image_height": None,
            "og_image_width": None,
            "og_title": None,
            "thumbnail_height": None,
            "thumbnail_url": None,
            "thumbnail_width": None,
            "title": "Wikipedia, the free encyclopedia",
            "type": "article",
            "version": "1.0"
        }

        self.surprise = models.Surprise.objects.create(
            link="http://whatever",
            description="A description"
        )

    def test_add_metadata_sets_canonical_url(self):
        self.surprise.add_metadata(self.metadata)
        self.assertEqual(self.surprise.link, "https://en.wikipedia.org/wiki/Main_Page")

    def test_add_metadata_sets_title(self):
        self.surprise.add_metadata(self.metadata)
        self.assertEqual(self.surprise.title, "Wikipedia, the free encyclopedia")

    def test_add_metadata_does_not_overwrite_description_if_there_is_no_description(self):
        self.surprise.add_metadata(self.metadata)
        self.assertEqual(self.surprise.description, "A description")


class GuardianMetadataTestCase(TestCase):
    def setUp(self):
        self.metadata = {
            "author_name": "Michael Hann",
            "canonical_url": "http://www.theguardian.com/music/musicblog/2015/oct/13/david-bowie-retirement-jay-z"
                             "-sinatra-meat-loaf-ozzy-osbourne",
            "description": "David Bowie has reportedly decided to retire from touring \u2013 and we believe him. But "
                           "it wouldn\u2019t be the first time a farewell pledge turned out not to be binding",
            "og_description": "David Bowie has reportedly decided to retire from touring \u2013 and we believe him. "
                              "But it wouldn\u2019t be the first time a farewell pledge turned out not to be binding",
            "og_image": "https://i.guim.co.uk/img/media/d09bc7ec2154ded732ab3f835a5d04afc8568382/0_687_3548_2127"
                        "/master/3548.jpg?w=1200&q=85&auto=format&sharp=10&s=6775811792d9d21580ba010cfbcfb1dd",
            "og_image_height": None,
            "og_image_width": None,
            "og_title": "From Bowie to Jay Z: the stars who forever left the stage \u2026 and came back",
            "thumbnail_height": None,
            "thumbnail_url": "https://i.guim.co.uk/img/media/d09bc7ec2154ded732ab3f835a5d04afc8568382/0_687_3548_2127"
                             "/master/3548.jpg?w=1200&q=85&auto=format&sharp=10&s=6775811792d9d21580ba010cfbcfb1dd",
            "thumbnail_width": None,
            "title": "From Bowie to Jay Z: the stars who forever left the stage \u2026 and came back | Music | The "
                     "Guardian",
            "type": "article",
            "version": "1.0"
        }

        self.surprise = models.Surprise.objects.create(
            link="http://whatever",
            description="A description"
        )

    def test_add_metadata_sets_title_but_prefers_og_title(self):
        self.surprise.add_metadata(self.metadata)
        self.assertEqual(self.surprise.title,
                         "From Bowie to Jay Z: the stars who forever left the stage \u2026 and came back")

    def test_add_metadata_does_overwrite_description_if_there_is_a_description(self):
        self.surprise.add_metadata(self.metadata)
        self.assertEqual(self.surprise.description,
                         "David Bowie has reportedly decided to retire from touring \u2013 and we believe him. But "
                         "it wouldn\u2019t be the first time a farewell pledge turned out not to be binding")

    def test_add_metadata_adds_author(self):
        self.surprise.add_metadata(self.metadata)
        self.assertEqual(self.surprise.author_name, 'Michael Hann')

    def test_add_metadata_adds_thumbnail(self):
        self.surprise.add_metadata(self.metadata)
        self.assertEqual(self.surprise.thumbnail_url,
                         "https://i.guim.co.uk/img/media/d09bc7ec2154ded732ab3f835a5d04afc8568382/0_687_3548_2127"
                         "/master/3548.jpg?w=1200&q=85&auto=format&sharp=10&s=6775811792d9d21580ba010cfbcfb1dd")


class RandomSurpriseTestCase(TestCase):

    def test_never_return_non_existing_link(self):
        non_existing = models.Surprise.objects.create(
            link="http://hjdsfhsdhfjdshfsdj.com",
            link_exists=False,
        )
        existing = models.Surprise.objects.create(
            link="http://fjhdsfhjdskhfjs.com",
            link_exists=True,
        )

        random_surprises = [models.get_random_surprise() for _ in range(100)]

        self.assertIn(existing, random_surprises)
        self.assertNotIn(non_existing, random_surprises)
