from datetime import datetime

from django.test import TestCase

from robber import expect

from activity.utils import utc_from_str, utc_to_str


class UtilsTestCase(TestCase):
    def test_utc_to_str(self):
        expect(utc_to_str(datetime(2018, 11, 28, 12, 11, 5))).to.eq('2018-11-28T12:11:05Z')

    def test_utc_from_str(self):
        expect(utc_from_str('2018-12-24T11:21:12Z')).to.eq(datetime(2018, 12, 24, 11, 21, 12))
