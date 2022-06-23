from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.Artist import Artist
from app_api.models.Genre import Genre
from rest_framework.permissions import AllowAny

class ArtistView(ViewSet):
    """Artist View"""
    # 1. We use the get method to retrieve the artist with the given pk.
    # 2. We use the ArtistSerializer to serialize the artist.
    # 3. We use the Response class to return the serialized artist.
    # 4. We use the status class to return a 404 status if the artist does not exist. 
    
    permission_classes = [AllowAny]
    
    def retrieve(self, request, pk):
        """Handle GET requests for single Artist
        
        Returns:
            Response -- JSON serialized Artist
        """
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all Artists

        Returns:
            Response -- JSON serialized list of artists
        """
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    # 1. We create a CreateArtistSerializer instance with the data from the request.
    # 2. We call the is_valid() method on the serializer, which will raise an exception if the data is invalid.
    # 3. We call the save() method on the serializer, which will save the data to the database.
    # 4. We return a Response object with the serialized data and a status code of 201 CREATED.
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized artist instance
        """
        serializer = CreateArtistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 1. We first import the Artist model.
    # 2. We then get the artist with the pk that was passed in the URL.
    # 3. We then update the artist's fields with the data that was passed in the request.
    # 4. We then save the artist.
    # 5. We then return a response with status code 204. 
    def update(self, request, pk):
        """Handle PUT requests for a artist

        Returns:
            Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.location = request.data["location"]
        artist.bio = request.data["bio"]
        artist.genre = Genre.objects.get(pk=pk)
        artist.music_link = request.data["music_link"]
        artist.website_link = request.data["website_link"]
        artist.photo_link = request.data["photo_link"]
        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a artist

        Returns:
            Response -- Empty body with 204 status code
        """
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    class Meta:
        model = Artist
        fields = ('id', 'name', 'location', 'bio', 'genre', 'music_link', 'website_link', 'photo_link')
        depth = 4
        
class CreateArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name', 'location', 'bio', 'genre', 'music_link', 'website_link', 'photo_link']        
        