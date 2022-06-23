from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.Skill_Level import SkillLevel

class SkillLevelView(ViewSet):
    """SkillLevel View"""
    
    permission_classes = []
    def retrieve(self, request, pk):
        """Handle GET requests for single SkillLevel
        
        Returns:
            Response -- JSON serialized SkillLevel
        """
        try:
            skill_level = SkillLevel.objects.get(pk=pk)
            serializer = SkillLevelSerializer(skill_level)
            return Response(serializer.data)
        except SkillLevel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all SkillLevels

        Returns:
            Response -- JSON serialized list of SkillLevels
        """
        skill_levels = SkillLevel.objects.all()
        serializer = SkillLevelSerializer(skill_levels, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized skill_level instance
        """
        serializer = CreateSkillLevelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a instrument

        Returns:
            Response -- Empty body with 204 status code
        """

        skill_level = SkillLevel.objects.get(pk=pk)
        skill_level.label = request.data["label"]
        skill_level.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a SkillLevel

        Returns:
            Response -- Empty body with 204 status code
        """
        instrument = SkillLevel.objects.get(pk=pk)
        instrument.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class SkillLevelSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    class Meta:
        model = SkillLevel
        fields = ('id', 'label')
        
class CreateSkillLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillLevel
        fields = ['label']        
        