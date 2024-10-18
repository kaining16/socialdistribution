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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import unquote

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

@api_view(['GET'])
def get_followers(request, author_serial):
    #get the author by author_serial
    try:
        author = Author.objects.get(username=author_serial)
    except Author.DoesNotExist:
        return Response({"detail": "No such author"}, status=status.HTTP_404_NOT_FOUND)

    #get all the followers of this author
    followers = author.followers.all()

    #generate the json of followers
    serializer = AuthorSerializer(followers, many=True)
    return Response({
        "type": "followers",
        "followers": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE', 'GET'])
def followers_api(request, author_serial, foreign_author_fqid):
    #get the author by author_serial
    try:
        author = Author.objects.get(username=author_serial)
    except Author.DoesNotExist:
        return Response({"detail": "No such author"}, status=status.HTTP_404_NOT_FOUND)

    #decode the encoded url
    decoded_fqid = unquote(foreign_author_fqid)

    #get the author by foreign_author_fqid
    try:
        foreign_author = Author.objects.get(fqid=decoded_fqid)
    except Author.DoesNotExist:
        return Response({"detail": "No such foreign author"}, status=status.HTTP_404_NOT_FOUND)

    #add the follower
    if request.method == 'PUT':
        if foreign_author == author:
            return Response({"detail": "Author cannot follow themselves"}, status=status.HTTP_400_BAD_REQUEST)
        elif foreign_author not in author.followers.all():
            author.add_follower(foreign_author)
            return Response({"detail": "Follow request accepted"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Already following"}, status=status.HTTP_400_BAD_REQUEST)

    #delete the follower
    elif request.method == 'DELETE':
        if foreign_author in author.followers.all():
            author.remove_follower(foreign_author)
            return Response({"detail": "Follower removed"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Can't delete, no such follower"}, status=status.HTTP_400_BAD_REQUEST)

    #get the follower
    elif request.method == 'GET':
        if foreign_author in author.followers.all():
            serializer = AuthorSerializer(foreign_author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No such follower"}, status=status.HTTP_404_NOT_FOUND)
