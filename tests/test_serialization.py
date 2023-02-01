import io
from django.test import TestCase
from django.urls import reverse
from rest_framework.parsers import JSONParser

from refs.models import Ref
from refs.serializers import RefSerializer
from rest_framework.test import APIRequestFactory
from refs.api_views import RefRetrieveAPIView, RefListAPIView


class TestRefSerializationt(TestCase):
    @classmethod
    def setUpClass(cls):
        Ref.objects.create(
            authors="S. Niyonzima et.al.",
            title="Low-energy collisions between electrons and BeH+: this is Ref 1",
            journal="Atomic Data and Nuclear Data Tables",
            volume="115-116",
            page_start="287",
            page_end="308",
            year=2017,
            doi="10.1016/j.adt.2016.09.002",
        )
        Ref.objects.create(
            authors="R. Ünal, P. Richard, I. Ben-Itzhak, C. L. Cocke, M. J. Singh, H. Tawara, N. Woody",
            title="Systematic study of charge-state and energy dependences of transfer-ionization to single-electron-capture ratios for F+q ions incident on He: this is Ref 2",
            journal="Physical Review A",
            volume="76",
            article_number="012710",
            year=2007,
            doi="10.1103/physreva.76.012710",
        )

        cls.factory = APIRequestFactory()
        super().setUpClass()

    def test_get_ref_from_api(self):
        request = self.factory.get("/api")
        view = RefRetrieveAPIView().as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")

        response = view(request, pk=2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 2")

        response = view(request, qid="B1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")
        self.assertNotContains(response, "this is Ref 2")

    def test_get_refs_from_api(self):
        request = self.factory.get("/api")
        view = RefListAPIView().as_view()
        response = view(request, pk=[1, 2])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")
        self.assertContains(response, "this is Ref 2")

        response = view(request, pk=[2])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 2")
        self.assertNotContains(response, "this is Ref 1")

        response = view(request, qid=["B1", "B2"])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")
        self.assertContains(response, "this is Ref 2")

        response = view(request, qid=["B1"])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")
        self.assertNotContains(response, "this is Ref 2")

    def test_endpoint(self):
        url = reverse("api")
        response = self.client.get(url + "?pk=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")
        self.assertNotContains(response, "this is Ref 2")

        response = self.client.get(url + "?pk=1&pk=2")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")
        self.assertContains(response, "this is Ref 2")

        response = self.client.get(url + "?qid=B2")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 2")
        self.assertNotContains(response, "this is Ref 1")

        response = self.client.get(url + "?qid=B1&qid=B2")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is Ref 1")
        self.assertContains(response, "this is Ref 2")

        doi = "10.1103/physreva.76.012710"
        response = self.client.get(url + f"?doi={doi}")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "this is Ref 1")
        self.assertContains(response, "this is Ref 2")

    def test_serialize_ref(self):
        ref = Ref.objects.get(pk=1)
        serializer = RefSerializer(ref)
        self.assertEqual(
            serializer.data,
            {
                "id": 1,
                "authors": "S. Niyonzima et.al.",
                "title": "Low-energy collisions between electrons and BeH+: this is Ref 1",
                "journal": "Atomic Data and Nuclear Data Tables",
                "volume": "115-116",
                "page_start": "287",
                "page_end": "308",
                "article_number": "",
                "year": 2017,
                "note": "",
                "doi": "10.1016/j.adt.2016.09.002",
                "bibcode": "",
                "url": "",
            },
        )

        refs = Ref.objects.all()
        serializer = RefSerializer(refs, many=True)
        self.assertEqual(len(serializer.data), 2)

    def test_deserialize_ref(self):
        ref_json = """{"authors":"J. Schweinzer, H. Winter","title":"Single electron capture from alkali atoms by slow doubly charged ions. I. He<sup>2+</sup>(0.5-6 keV)-Li, Na, K-one-electron processes","journal":"Journal of Physics B: Atomic, Molecular and Optical Physics","volume":"23","page_start":"3881","page_end":"3898","article_number":"","year":1990,"note":"","doi":"10.1088/0953-4075/23/21/021","bibcode":"1990JPhB...23.3881S","url":"https://dx.doi.org/10.1088/0953-4075/23/21/021"}"""
        stream = io.BytesIO(bytes(ref_json, encoding="utf8"))
        data = JSONParser().parse(stream)
        serializer = RefSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        ref = serializer.save()
        self.assertEqual(ref.pk, 3)

        ref = Ref.objects.get(pk=3)
        self.assertEqual(
            ref.title,
            "Single electron capture from alkali atoms by slow doubly charged ions. I. He<sup>2+</sup>(0.5-6 keV)-Li, Na, K-one-electron processes",
        )
        ref = Ref.objects.get(doi="10.1088/0953-4075/23/21/021")
        self.assertEqual(ref.authors, "J. Schweinzer, H. Winter")
