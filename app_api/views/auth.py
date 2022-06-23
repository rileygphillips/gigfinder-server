from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from app_api.models.Artist import Artist
from app_api.models.Genre import Genre
from app_api.models.Instrument import Instrument
from app_api.models.Musician import Musician
from app_api.models.Skill_Level import SkillLevel


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        try:
            is_artist = Artist.objects.get(user=authenticated_user)
        
        except Artist.DoesNotExist:
            is_artist = False
        # TODO: If you need to return more information to the client, update the data dict
        data = {
            'valid': True,
            'token': token.key,
            'is_artist': bool(is_artist)
        }
    else:
        data = { 'valid': False }
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # TODO: this is only adding the username and password, if you want to add in more user fields like first and last name update this code
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email']
    )
    
    if request.data['is_artist'] == True:
        # Now save the extra info in the app_api_artist table
        artist = Artist.objects.create(
            name = request.data["name"],
            location = request.data["location"],
            bio = request.data["bio"],
            genre = Genre.objects.get(pk=request.data["genre"]),
            music_link = request.data["music_link"],
            website_link = request.data["website_link"],
            photo_link = request.data["photo_link"],
            user = new_user
        )
    
    if request.data['is_artist'] == False:
        # Now save the extra info in the app_api_musician table
        musician = Musician.objects.create(
            skill_level = SkillLevel.objects.get(pk=request.data["skill_level"]),
            first_name = request.data["first_name"],
            last_name = request.data["last_name"],
            location = request.data["location"],
            bio = request.data["bio"],
            email = request.data["email"],
            resume_link = request.data["resume_link"],
            audition_video_link = request.data["audition_video_link"],
            instruments = Instrument.objects.get(pk=request.data["instrument"]),
            photo_link = request.data["photo_link"],
            musician = new_user
        )
    
    
    token = Token.objects.create(user=new_user)
    # TODO: If you need to send the client more information update the data dict
    
    data = { 'token': token.key }
    return Response(data, status=status.HTTP_201_CREATED)
