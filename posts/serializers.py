from rest_framework import serializers
from .models import Post, Like, Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'user', 'text', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author         = UserSerializer(read_only=True)
    likes_count    = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    liked_by_me    = serializers.SerializerMethodField()
    image          = serializers.SerializerMethodField()

    class Meta:
        model  = Post
        fields = [
            'id', 'author', 'content', 'image',
            'likes_count', 'comments_count', 'liked_by_me',
            'created_at',
        ]

    def get_liked_by_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = ['content', 'image']

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(author=user, **validated_data)