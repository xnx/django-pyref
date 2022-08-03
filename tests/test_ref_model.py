from django.test import TestCase
from refs.models import Ref


class TestRef(TestCase):
    def setUp(self):
        self.doi = "10.1016/j.adt.2016.09.002"
        Ref.objects.create(
            authors="S. Niyonzima et.al.",
            title="Low-energy collisions between electrons and BeH+",
            journal="Atomic Data and Nuclear Data Tables",
            volume="115-116",
            page_start="287",
            page_end="308",
            year=2017,
            doi=self.doi,
        )

    def test_get_ref(self):
        ref = Ref.objects.get(doi=self.doi)
        self.assertEqual(ref.year, 2017)
