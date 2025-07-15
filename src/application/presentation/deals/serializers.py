# mypy: disable-error-code="type-arg"
# pyright: reportMissingTypeArgument=false
from rest_framework import serializers


class DealCreateSerializer(serializers.Serializer):
    """Serializer for creating a deal."""

    title = serializers.CharField(max_length=255)
    company_id = serializers.IntegerField()
    value = serializers.DecimalField(max_digits=12, decimal_places=2)
    tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_null=True
    )
    distributor_id = serializers.IntegerField(required=False, allow_null=True)


class DealUpdateSerializer(serializers.Serializer):
    """Serializer for updating a deal."""

    deal_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255, required=False, allow_null=True)
    distributor_id = serializers.IntegerField(required=False, allow_null=True)
    tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_null=True
    )
    value = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )


class DealIdSerializer(serializers.Serializer):
    """Serializer for deal id only (used for get/delete by id)."""

    deal_id = serializers.IntegerField()


class DealSerializer(serializers.Serializer):
    """Serializer for deal output (minimal example)."""

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    company_id = serializers.IntegerField()
    value = serializers.DecimalField(max_digits=12, decimal_places=2)
    tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_null=True
    )
    distributor_id = serializers.IntegerField(required=False, allow_null=True)
