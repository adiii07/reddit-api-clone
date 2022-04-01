from rest_framework import serializers
from feed.models import Post, Reply, Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ('post', 'user')

class PostSerializer(serializers.ModelSerializer):    
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        
class ReplySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Reply
        exclude = ('post', )
        