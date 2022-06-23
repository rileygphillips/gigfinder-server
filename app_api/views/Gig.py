from django.db.models.functions import Lower
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.Genre import Genre
from app_api.models.Gig import Gig
from app_api.models.Artist import Artist
from rest_framework.decorators import action
from app_api.models.Instrument import Instrument

from app_api.models.Musician import Musician
from app_api.models.Skill_Level import SkillLevel

class GigView(ViewSet):
    """Musician View"""
    permission_classes = []
    def retrieve(self, request, pk):
        """Handle GET requests for single Gig
        
        Returns:
            Response -- JSON serialized Gig
        """
        try:
            gig = Gig.objects.get(pk=pk)
            serializer = GigSerializer(gig)
            return Response(serializer.data)
        except Gig.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all Gig

        Returns:
            Response -- JSON serialized list of Gig
        """
        gigs = Gig.objects.all()
        user = request.query_params.get('user', None)
        if user is not None:
            gigs = gigs.filter(artist=artist)
        artist = request.query_params.get('artist', None)
        if artist is not None:
            gigs = gigs.filter(artist=artist)
        for gig in gigs:
            gig.is_authorized=gig.artist.user==request.user
            
        serializer = GigSerializer(gigs, many=True)
        return Response(serializer.data)
    
    @action(methods=["get"], detail=False)
    def current_artist_list(self, request):
            artist = Artist.objects.get(user_id=request.auth.user.id)
            gigs = Gig.objects.filter(artist=artist)
            
            for gig in gigs:
                gig.is_authorized=gig.artist==artist
            
            serializer = GigSerializer(gigs, many=True)
            return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Gig instance
        """
        artist = Artist.objects.get(user_id=request.auth.user.id)
        serializer = CreateGigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(artist=artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a Gig

        Returns:
            Response -- Empty body with 204 status code
        """

        gig = Gig.objects.get(pk=pk)
        gig.skill_level_needed = SkillLevel.objects.get(pk=request.data["skill_level_needed"])
        gig.gig_name = request.data["gig_name"]
        gig.location = request.data["location"]
        gig.date = request.data["date"]
        gig.description = request.data["description"]
        gig.genre = Genre.objects.get(pk=request.data["genre"])
        gig.venue = request.data["venue"]
        gig.instruments_needed = Instrument.objects.get(pk=request.data["instruments_needed"])
        gig.photo_link = request.data["photo_link"]
        gig.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def applied_gigs(self, request, pk):
        """Post request for a musician to apply to gig"""
        musician = Musician.objects.get(musician=request.auth.user)
        gig = Gig.objects.get(pk=pk)
        gig.gigs_submitted_to.add(musician)
        return Response({'message': 'Gig Applied For'}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a gig

        Returns:
            Response -- Empty body with 204 status code
        """
        gig = Gig.objects.get(pk=pk)
        gig.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class GigSerializer(serializers.ModelSerializer):
    """JSON serializer for musicians
    """
    class Meta:
        model = Gig
        fields = ('id', 'artist', 'gig_name', 'location', 'date', 'description', 'genre', 'venue', 'skill_level_needed', 'instruments_needed', 'photo_link')
        depth = 4
        
class CreateGigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gig
        fields = ['gig_name', 'location', 'date', 'description', 'genre', 'venue', 'skill_level_needed', 'instruments_needed', 'photo_link'] 