
from rest_framework import serializers
from .models import StudentAnswer

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'