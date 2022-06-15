from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.Instrument import Instrument

class InstrumentView(ViewSet):
    """Instrument View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single Instrument
        
        Returns:
            Response -- JSON serialized Instrument
        """
        try:
            instrument = Instrument.objects.get(pk=pk)
            serializer = InstrumentSerializer(instrument)
            return Response(serializer.data)
        except Instrument.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all instrument

        Returns:
            Response -- JSON serialized list of instrument
        """
        instruments = Instrument.objects.all()
        serializer = InstrumentSerializer(instruments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instrument instance
        """
        serializer = CreateInstrumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a instrument

        Returns:
            Response -- Empty body with 204 status code
        """

        instrument = Instrument.objects.get(pk=pk)
        instrument.label = request.data["label"]
        instrument.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a instrument

        Returns:
            Response -- Empty body with 204 status code
        """
        instrument = Instrument.objects.get(pk=pk)
        instrument.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class InstrumentSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    class Meta:
        model = Instrument
        fields = ('id', 'label')
        
class CreateInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['label']        
        