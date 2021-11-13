from .models import StreetRisk
from rest_framework import serializers

class StreetRiskSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="streetrisk-detail")
    class Meta:
        model = StreetRisk
        fields = ('__all__')