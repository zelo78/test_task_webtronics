from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from main.models import Post
from main.serializers import (
    PostSerializer,
    PostForAuthorSerializer,
    PostCreateUpdateSerializer,
    UserCreateSerializer,
    UserInfoSerializer,
)


class UserViewsetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow metadata
        if request.method in ("HEAD", "OPTIONS"):
            return True

        # Allow register new users
        if request.method == "POST":
            return True

        # All other operation (include GET) require authentication
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins can do anything and
        # user cad patch themselves
        return request.user.is_staff or (
            request.method in ["PUT", "PATCH"] and obj == request.user
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created, viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [UserViewsetPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ["create"]:
            serializer_class = UserCreateSerializer

        return serializer_class

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data.get("password"))
        user.save()


class IsOwnerOrStaffOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Object-level permission to allow staff or owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # We allow like and unlike from any authenticated Users
        if request.user.is_authenticated and view.action in ["like", "unlike"]:
            return True

        # Only author and staff can edit posts
        return request.user.is_staff or obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created")
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ["author"]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action in ["retrieve"]:
            user = self.request.user
            pk = self.kwargs.get("pk")
            if user.is_authenticated and (
                user.is_staff or Post.objects.filter(pk=pk, author=user).exists()
            ):
                serializer_class = PostForAuthorSerializer
        elif self.action in ["create", "update", "partial_update"]:
            serializer_class = PostCreateUpdateSerializer

        return serializer_class

    @action(detail=True, methods=["patch"])
    def like(self, request, pk=None):
        user = self.request.user
        post = self.get_object()
        if user.is_authenticated and user != post.author:
            post.likes.add(user)
            post.unlikes.remove(user)

        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def unlike(self, request, pk=None):
        user = self.request.user
        post = self.get_object()
        if user.is_authenticated and user != post.author:
            post.unlikes.add(user)
            post.likes.remove(user)

        serializer = self.get_serializer(post)
        return Response(serializer.data)
