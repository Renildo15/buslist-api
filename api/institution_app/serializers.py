from rest_framework import serializers

from .models import Institution, InstitutionAddress


class InstitutionAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionAddress
        fields = "__all__"


class InstitutionAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionAddress
        fields = ["address", "city", "state", "zip_code"]


class InstitutionSerializer(serializers.ModelSerializer):
    address = InstitutionAddressSerializer()

    class Meta:
        model = Institution
        fields = "__all__"


class InstitutionCreateSerializer(serializers.ModelSerializer):
    address = InstitutionAddressCreateSerializer()

    class Meta:
        model = Institution
        fields = ["name", "phone_number", "acronym", "address", "in_vacation"]

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = InstitutionAddress.objects.create(**address_data)
        institution = Institution.objects.create(address=address, **validated_data)

        return institution
