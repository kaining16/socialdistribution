from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomAuthorCreationForm
from .models import Author
from django.shortcuts import render, redirect
from .forms import CustomAuthorCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def register(request):
    #simple register
    if request.method == 'POST':
        form = CustomAuthorCreationForm(request.POST, request=request)  
        if form.is_valid():
            author = form.save()  
            #login(request, author)
    else:
        form = CustomAuthorCreationForm(request=request)  
    return render(request, 'register.html', {'form': form})

def login_view(request):
    #simple login
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'login.html')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@api_view(['GET'])
def get_authors(request):
    "get all authors"
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response({
        "type": "authors",
        "authors": serializer.data
    })

@api_view(['GET', 'PUT'])
def author_profile(request, author_serial):
    "get, modify a specific author"
    "local"
    try:
        author = Author.objects.get(username=author_serial)
    except Author.DoesNotExist:# if can't find author with this username
        author = None  
    #get
    if request.method == 'GET':
        if author is None:
            return Response({"detail": "No such author"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    #put
    elif request.method == 'PUT':
        #can only update an existing author, can not create an author
        if author is None:
            return Response({"detail": "No such author, create is forbidden"}, status=status.HTTP_404_NOT_FOUND) 
        else:
            serializer = AuthorSerializer(author, data=request.data, partial=True)  

        #ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"detail": "not login"}, status=status.HTTP_403_FORBIDDEN)
        
        #check if id exists and matches the login author
        request_id = request.data.get('id', None)
        if request_id == None or request_id != request.user.fqid :
            return Response({"detail": "not match current author"}, status=status.HTTP_400_BAD_REQUEST)
        
        #check if host matches the host we're making the request to
        request_host = request.data.get('host', None)
        if request_host == None or request_host != author.host:
            return Response({"detail": "host not match"}, status=status.HTTP_400_BAD_REQUEST)
        
         #check if type is "author"
        request_type = request.data.get('type', None)
        if request_type == None or request_type != "author":
            return Response({"detail": "type should be author"}, status=status.HTTP_400_BAD_REQUEST)
        
        #if it's valid, change profile
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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