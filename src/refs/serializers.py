from .models import Ref
from rest_framework import serializers


class RefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref
        fields = (
            "id",
            "authors",
            "title",
            "journal",
            "volume",
            "page_start",
            "page_end",
            "article_number",
            "year",
            "note",
            "doi",
            "bibcode",
            "url",
        )
