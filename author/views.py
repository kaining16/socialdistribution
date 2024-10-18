from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import status

@api_view(['GET'])
def get_authors(request):
    
    
    authors = Author.objects.all()
    
    
    serializer = AuthorSerializer(authors, many=True)
    
    
    return Response({
        "type": "authors",
        "authors": serializer.data
    })

# GET and PUT for AUTHOR_SERIAL
@api_view(['GET', 'PUT'])
def author_profile(request, pk):
    
    try:
        
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        author = None  

    if request.method == 'GET':
        if author is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if author is None:
            serializer = AuthorSerializer(data=request.data)  
        else:
            serializer = AuthorSerializer(author, data=request.data, partial=True)  

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if author is None else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# GET for AUTHOR_FQID
@api_view(['GET'])
def author_profile_fqid(request, author_fqid):
    try:
        author = Author.objects.get(id=author_fqid)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AuthorSerializer(author)
    return Response(serializer.data)


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomAuthorCreationForm
from .models import Author

from django.shortcuts import render, redirect
from .forms import CustomAuthorCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomAuthorCreationForm(request.POST, request=request)  
        if form.is_valid():
            author = form.save()  
            
    else:
        form = CustomAuthorCreationForm(request=request)  
    return render(request, 'register.html', {'form': form})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Author
from .serializers import FollowerSerializer
from urllib.parse import unquote

@api_view(['GET', 'PUT', 'DELETE'])
def followers_list(request, author_serial):
    try:
        author = Author.objects.get(pk=author_serial)
    except Author.DoesNotExist:
        return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        followers = author.followers.all()
        serializer = FollowerSerializer(followers, many=True)
        return Response({"type": "followers", "followers": serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        foreign_author_fqid = request.data.get('id')  
        try:
            foreign_author = Author.objects.get(fqid=foreign_author_fqid)
        except Author.DoesNotExist:
            return Response({"detail": "Foreign author not found"}, status=status.HTTP_404_NOT_FOUND)

        author.followers.add(foreign_author)
        return Response({"detail": "Followed successfully"}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        foreign_author_fqid = request.data.get('id')  
        try:
            foreign_author = Author.objects.get(fqid=foreign_author_fqid)
        except Author.DoesNotExist:
            return Response({"detail": "Foreign author not found"}, status=status.HTTP_404_NOT_FOUND)

        author.followers.remove(foreign_author)
        return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def check_follower(request, author_serial, foreign_author_fqid):
    foreign_author_fqid = unquote(foreign_author_fqid)  

    try:
        author = Author.objects.get(pk=author_serial)
    except Author.DoesNotExist:
        return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        foreign_author = Author.objects.get(fqid=foreign_author_fqid)
    except Author.DoesNotExist:
        return Response({"detail": "Foreign author not found"}, status=status.HTTP_404_NOT_FOUND)

    if foreign_author in author.followers.all():
        serializer = FollowerSerializer(foreign_author)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Not following"}, status=status.HTTP_404_NOT_FOUND)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Author, FollowRequest
from .serializers import FollowRequestSerializer
from urllib.parse import unquote

@api_view(['POST'])
def receive_follow_request(request, author_serial):
    
    try:
        target_author = Author.objects.get(id=unquote(author_serial)) 
    except Author.DoesNotExist:
        return Response({'error': 'Target author not found'}, status=status.HTTP_404_NOT_FOUND)

    
    serializer = FollowRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    if serializer.validated_data['object']['id'] != target_author.fqid:
        return Response({
        'error': f"Object id '{serializer.validated_data['object']['id']}' does not match the author_serial '{target_author.id}'"
    }, status=status.HTTP_400_BAD_REQUEST)

   
    serializer.save()

    
    return Response(serializer.data, status=status.HTTP_201_CREATED)