
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, UserType


class UserTypeSerializer(serializers.ModelSerializer):
    """ Serializer User type model """

    class Meta:
        """ meta """
        model = UserType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """ Serialize user model """
    user_type = UserTypeSerializer(read_only=True)
    user_type_id = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        """ user type string to user type id """
        if isinstance(data.get('user_type_id'), str):
            user_type = UserType.objects.filter(code=data['user_type_id'].lower()).last()
            if user_type is None:
                raise ValidationError({'user_type': "Not defined"})
            data['user_type_id'] = user_type.id
        return super().to_internal_value(data)

    class Meta(object):
        """ Meta """
        model = User
        fields = ('id', 'email', 'name', 'surname', 'password', 'is_superuser', 'user_type', 'user_type_id')
        extra_kwargs = {'password': {'write_only': True}, 'is_superuser': {'read_only': True}}

    def create(self, validated_data):
        """ create user """
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            user_type_id=validated_data['user_type_id'],
            password=validated_data['password']
        )
        return user
