from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Includes read-only user information nested inside the profile response.
    """

    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    bio = serializers.CharField(source='user.bio', read_only=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'bio',
            'profile_picture',
            'location',
            'website',
            'followers_count',
            'following_count',
            'created_at',
        ]
        read_only_fields = ['id', 'followers_count', 'following_count', 'created_at']

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating profile and user information.
    Allows updating fields across both the User and Profile models.
    """

    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    bio = serializers.CharField(source='user.bio', required=False, allow_blank=True)
    profile_picture = serializers.ImageField(source='user.profile_picture', required=False)

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'bio',
            'profile_picture',
            'location',
            'website',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance