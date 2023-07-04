from django.contrib.auth.models import User
from rest_framework import serializers

class ApiSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username']).first()
        if not user or not user.check_password(attrs['password']):
            raise serializers.ValidationError('Credenciais inválidas.')
        attrs['user'] = user
        return attrs

