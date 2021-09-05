from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions

# custom permission 
class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only....custom permission de foued'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class PostList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly] # views permission like IsAdminUser..........
    queryset = Post.postobjects.all() # ou postobjects notre manager au lieu de objects
    serializer_class = PostSerializer
        # DjangoModelPermissionsOrAnonReadOnly # permission model django = qu'on etabli dans admin=>group=>user
        # DjangoModelPermissions # permission model django


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
