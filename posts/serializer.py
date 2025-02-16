from rest_framework import serializers

from .models import Post, Comment, Like, CommentReplay, LikeComment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'title', 'caption', 'is_active', 'created_time')
        extra_kwargs = {
            'user': {'read_only':True}
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'user', 'text')
        extra_kwargs = {
            'user': {'read_only':True},
            'post': {'read_only': True},
            #'replay': {'required': False}
        }


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user', 'is_liked')
        extra_kwargs = {
            'user': {'read_only':True},
            'post': {'read_only': True},
            'is_liked': {'required':False}
        }

class CommentReplaySerializer(serializers.ModelSerializer):
    comment = CommentSerializer
    class Meta:
        model = CommentReplay
        fields = ('user', 'comment', 'text')
        extra_kwargs = {
            'user': {'read_only':True},
            'comment': {'read_only': True}
        }

class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = ('comment', 'user', 'is_liked')
        extra_kwargs = {
            'user': {'read_only':True},
            'comment': {'read_only': True},
            'is_liked': {'required':False}
        }