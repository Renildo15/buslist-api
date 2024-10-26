from rest_framework import serializers

from .models import BusStop, BusStopAddress


class BusStopAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStopAddress
        fields = ["address", "neighborhood","city", "state", "zip_code"]


class BusStopAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStopAddress
        fields = "__all__"


class BusStopCreateSerializer(serializers.ModelSerializer):
    address = BusStopAddressCreateSerializer()

    class Meta:
        model = BusStop
        fields = ["name", "address"]

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = BusStopAddress.objects.create(**address_data)
        bus_stop = BusStop.objects.create(address=address, **validated_data)

        return bus_stop


class BusStopSerializer(serializers.ModelSerializer):
    address = BusStopAddressSerializer()

    class Meta:
        model = BusStop
        fields = "__all__"
