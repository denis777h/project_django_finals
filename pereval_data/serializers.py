from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import (PerevalUser, Image, PerevalLevel, PerevalCoordinate, PerevalAdded)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalUser
        fields = ('__all__')
        pass


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('__all__')


class LeverSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalLevel
        fields = ('__all__')


class CoordinatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalCoordinate
        fields = ('__all__')
        read_only_fields = ['latitude', 'longitude', 'height', 'coordinates', ]

        pass


class PerevalSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    status = serializers.CharField(read_only=True)
    image = ImageSerializer(many=False, read_only=True)
    lever = LeverSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    coordinates = CoordinatSerializer(many=True, read_only=True)

    class Meta:
        model = PerevalAdded
        fields = ('__all__')

        def __init__(self):
            self.instance = None

        def create(self, validated_data, *args, **kwargs):
            user = validated_data.pop('user')
            coord = validated_data.pop('coord')
            image = validated_data.pop('image')
            coord = PerevalCoordinate.objects.create(**coord)
            pereval = PerevalAdded.objects.create(**validated_data, coord=coord, user=user)
            user = PerevalAdded.objects.get_or_create(**user)
            created = PerevalAdded.objects.get_or_create(**user)

            for image in image:
                title = image.pop('title')
                data = image.pop('data')
                image.objects.create(pereval=pereval, title=title, data=data)
                pass
            return pereval

        def validate(self, value, instance, validated_data):
            user_data = value['user']
            instance = instance
            validated_data = validated_data
            if self.instance:
                if (user_data['email'] != self.instance.user.email
                        or user_data['surname'] != self.instance.user.surname
                        or user_data['name'] != self.instance.user.name
                        or user_data['otc'] != self.instance.user.otc
                        or user_data['phone'] != self.instance.user.phone):
                    raise serializers.ValidationError()
                return value
            if self.instance and self.instance.status != 'new':
                print({"message": "Данный перевал принят в работу, информацию о нем уже нельзя поменять",
                       "state": "0"})
            if any(user_data[field] != getattr(user_data, field) for field in
                   ('fam', 'name', 'otc', 'email', 'phone')):
                print({"message": "Информацию о пользователе нельзя изменять.", "state": "0"})
                if error_messages:
                    raise ValidationError(error_messages)
                validated_data['message'] = "Данные успешно изменены!"
                validated_data['state'] = "1"
            return validated_data
