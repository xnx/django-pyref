from django.test import TestCase
from refs.utils import canonicalize_doi


class TestUtils(TestCase):
    def test_canonicalization(self):
        doi = "10.1016/j.adt.2016.09.002"
        for prefix in (
            "http://doi.org/",
            "https://doi.org/",
            "http://dx.doi.org/",
            "https://dx.doi.org/",
        ):
            self.assertEqual(canonicalize_doi(f"{prefix}{doi}"), doi)
