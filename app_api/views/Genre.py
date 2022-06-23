from django.db.models.functions import Lower
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.Genre import Genre

class GenreView(ViewSet):
    """Genre View"""
    permission_classes = []
    
    def retrieve(self, request, pk):
        """Handle GET requests for single Genre
        
        Returns:
            Response -- JSON serialized Genre
        """
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all Genre

        Returns:
            Response -- JSON serialized list of Genre
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized genre instance
        """
        serializer = CreateGenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a genre

        Returns:
            Response -- Empty body with 204 status code
        """

        genre = Genre.objects.get(pk=pk)
        genre.label = request.data["label"]
        genre.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a genre

        Returns:
            Response -- Empty body with 204 status code
        """
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    class Meta:
        model = Genre
        fields = ('id', 'label')
        
class CreateGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['label']        
        