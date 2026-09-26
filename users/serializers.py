from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    posts_count     = serializers.ReadOnlyField()
    is_following    = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            'id', 'username', 'email', 'bio',
            'avatar', 'banner',
            'followers_count', 'following_count', 'posts_count',
            'is_following',
        ]
        extra_kwargs = {
            'avatar': {'required': False, 'allow_null': True},
            'banner': {'required': False, 'allow_null': True},
        }

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(pk=request.user.pk).exists()
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            if instance.avatar:
                url = instance.avatar.url
                # Se já for URL absoluta (Cloudinary), não usa build_absolute_uri
                data['avatar'] = url if url.startswith('http') else request.build_absolute_uri(url)
            if instance.banner:
                url = instance.banner.url
                data['banner'] = url if url.startswith('http') else request.build_absolute_uri(url)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'As senhas não coincidem.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user