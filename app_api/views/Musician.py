from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Instrument
from app_api.models.Skill_Level import SkillLevel
from app_api.models.Musician import Musician
from rest_framework.permissions import AllowAny
class MusicianView(ViewSet):
    """Musician View"""
    permission_classes = [AllowAny]
    def retrieve(self, request, pk):
        """Handle GET requests for single Musician
        
        Returns:
            Response -- JSON serialized Musician
        """
        try:
            musician = Musician.objects.get(pk=pk)
            serializer = MusicianSerializer(musician)
            return Response(serializer.data)
        except Musician.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all Musicians

        Returns:
            Response -- JSON serialized list of Musicians
        """
        musicians = Musician.objects.all()
        serializer = MusicianSerializer(musicians, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Musician instance
        """
        serializer = CreateMusicianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a Musician

        Returns:
            Response -- Empty body with 204 status code
        """

        musician = Musician.objects.get(pk=pk)
        musician.skill_level = SkillLevel.objects.get(pk=pk)
        musician.first_name = request.data["first_name"]
        musician.last_name = request.data["last_name"]
        musician.location = request.data["location"]
        musician.bio = request.data["bio"]
        musician.email = request.data["email"]
        musician.resume_link = request.data["resume_link"]
        musician.audition_video_link = request.data["audition_video_link"]
        musician.instruments = Instrument.objects.get(pk=pk)
        musician.photo_link = request.data["photo_link"]
        musician.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a musician

        Returns:
            Response -- Empty body with 204 status code
        """
        musician = Musician.objects.get(pk=pk)
        musician.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class MusicianSerializer(serializers.ModelSerializer):
    """JSON serializer for musicians
    """
    class Meta:
        model = Musician
        fields = ('id', 'musician', 'first_name', 'last_name', 'location', 'bio', 'email', 'skill_level', 'resume_link', 'audition_video_link', 'instruments', 'photo_link')
        depth = 4
        
class CreateMusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musician
        fields = ['first_name', 'last_name', 'location', 'bio', 'email', 'skill_level', 'resume_link', 'audition_video_link', 'instruments', 'photo_link'] 