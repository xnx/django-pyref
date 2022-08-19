from rest_framework import generics

from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from .models import Ref
from .serializers import RefSerializer


class RefRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Ref.objects.all()
    serializer_class = RefSerializer

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends

        if "qid" in self.kwargs:
            pk = int(self.kwargs["qid"][1:])
        else:
            pk = self.kwargs["pk"]

        obj = get_object_or_404(queryset, pk=pk)  # Lookup the object
        return obj


class RefListAPIView(generics.ListAPIView):
    queryset = Ref.objects.all()
    serializer_class = RefSerializer

    def get_queryset(self):

        if doi := self.kwargs.get("doi"):
            return get_list_or_404(self.queryset, doi__in=doi)

        if qid := self.kwargs.get("qid"):
            pks = [int(s[1:]) for s in qid]
        elif pk := self.kwargs.get("pk"):
            pks = pk
        else:
            raise ValueError(f"Invalid query keyword in {self.kwargs}.")

        return get_list_or_404(self.queryset, pk__in=pks)


def endpoint(request):
    kwargs = request.GET
    return RefListAPIView.as_view()(request, **kwargs)
