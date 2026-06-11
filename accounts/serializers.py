from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'role', 'telephone', 'region', 'date_naissance'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role',
            'telephone', 'region', 'date_naissance',
            'photo_profil', 'is_online', 'date_joined'
        ]
        read_only_fields = ['id', 'role', 'date_joined']

class ChangePasswordSerializer(serializers.Serializer):
    ancien_password = serializers.CharField(required=True)
    nouveau_password = serializers.CharField(
        required=True, validators=[validate_password]
    )
