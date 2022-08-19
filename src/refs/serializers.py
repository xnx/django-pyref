from .models import Ref
from rest_framework import serializers


class RefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref
        fields = (
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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {instance.qualified_id: ret}
