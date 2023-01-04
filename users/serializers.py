from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['id', 'user', 'address_type', 'default']

    def create(self, validated_data):
        user = self.context.get('user')
        address_type = self.context.get('address_type')
        save_info = self.context.get('save_info')

        address = Address.objects.create(
            user=user,
            address_type=address_type,
            **validated_data
        )
        if save_info == True:
            address.default = True
            address.save()
        return address
