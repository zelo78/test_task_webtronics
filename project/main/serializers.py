from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "url", "username", "first_name", "last_name", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "url",
            "title",
            "text",
            "created",
            "edited",
            "author",
            "likes_count",
            "unlikes_count",
        ]


class PostForAuthorSerializer(serializers.ModelSerializer):
    likes = UserInfoSerializer(many=True)
    unlikes = UserInfoSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "url",
            "title",
            "text",
            "created",
            "edited",
            "author",
            "likes_count",
            "unlikes_count",
            "likes",
            "unlikes",
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "url",
            "title",
            "text",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(**validated_data, author=user)
        return post
