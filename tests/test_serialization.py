from django.test import TestCase
from django.urls import reverse
from refs.models import Ref
from rest_framework.test import APIRequestFactory
from refs.api_views import RefRetrieveAPIView, RefListAPIView


class TestRefSerializationt(TestCase):
    def setUp(self):
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

        self.factory = APIRequestFactory()
        super().setUpClass()

    def test_get_ref(self):
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

    def test_get_refs(self):
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
