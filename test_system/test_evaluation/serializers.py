from rest_framework import serializers, viewsets
from .models import StudentExam

class StudentAnswerSerializer(serializers.ModelSerializer):
    no_of_std_id=serializers.ReadOnlyField()
    class Meta:
        model = StudentExam
        fields = '__all__'

# class StudentAnswerViewSet(viewsets.ModelViewSet):
#     queryset = StudentExam.objects.all()
#     serializer_class = StudentAnswerSerializer
