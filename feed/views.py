from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from feed.models import *
from feed.serializers import *
from feed.pagination import PostsPagination
from feed.permissions import IsAuthorOrReadOnly


class VotePost(APIView):
    
    def post(self, serializer, pk, action):
        user = self.request.user
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'errors': 'Post does not exist'})
        
        vote_queryset = Vote.objects.filter(user=user, post=post)
        if vote_queryset.exists():
            if vote_queryset[0].action_type != action:
                vote_queryset.delete()
            else: 
                return Response({'errors': 'Already voted'})
    
        if action == "U" or action == 'D':
            new_vote = Vote.objects.create(user=user, post=post, action_type=action)
            new_vote.save()
            serializer = VoteSerializer(new_vote)
        else:
            return Response({'errors': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)
        
        post.votes = Vote.objects.filter(post=post, action_type='U').count() - Vote.objects.filter(post=post, action_type='D').count()
        post.save()
        
        return Response({'votes': post.votes,
                         'upvotes': len(Vote.objects.filter(post=post, action_type='U')),
                         'downvotes': len(Vote.objects.filter(post=post, action_type='D'))}, status=status.HTTP_201_CREATED)            
        

class RemoveVote(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, pk):
        post = Post.objects.get(pk=pk)
        user = self.request.user
        vote = Vote.objects.filter(post=post, user=user)
        if vote.exists():
            vote.delete()
        else:
            return Response({'errors': 'Post has not been voted'})
        return Response(status=status.HTTP_200_OK)
        

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['votes']
    pagination_class = PostsPagination    
    
class PostCreate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

class ReplyList(generics.ListCreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reply.objects.filter(post__id=pk)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk') 
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            
        author = self.request.user
        serializer.save(post=post, author=author)

class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthorOrReadOnly]
    
