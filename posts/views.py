from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializer import PostSerializer, CommentSerializer, LikeSerializer, CommentReplaySerializer, LikeCommentSerializer
from django.contrib.auth.models import User


class PostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExists:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.filter(is_active=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class CommentView(APIView):
    permission_classes = [IsAuthenticated]


    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return False

    def get(self, request, pk):
        post = self.get_post(pk=pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post=post, is_approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    def post(self, request, pk):
        post = self.get_post(pk=pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return False

    def get(self, request, pk):
        post = self.get_post(pk=pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = post.likes.filter(is_liked=True).count()
        return Response({'likes':likes})

    def post(self, request, pk):
        post = self.get_post(pk=pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentReplayView(APIView):
    permission_classes = [IsAuthenticated]

    def get_comment(self, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return comment

    def get(self, request, pk):
        comment = self.get_comment(pk=pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        replay = comment.replays.all()
        serializer = CommentReplaySerializer(replay, many=True)
        return Response(serializer.data)
    def post(self, request, pk):
        comment = self.get_comment(pk=pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentReplaySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(comment=comment, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(user=request.user)
        try:
            comment  = user.user_comment.all()
        except Comment.DoesNotExsist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'user-comments':comment})


class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return False

    def get(self, request, pk):
        comment = self.get_comment(pk=pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = comment.like_comment.filter(is_liked=True).count()
        return Response({'likes':likes})

    def post(self, request, pk):
        comment = self.get_comment(pk=pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LikeCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(comment=comment, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)