from .models import Student, Subject, Score
from rest_framework import serializers

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'average_overall']

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class ScoreSerializer(serializers.HyperlinkedModelSerializer):    
    student_name = serializers.CharField(source='student.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Score
        fields = ['student', 'subject', 'score', 'student_name', 'subject_name']

    def validate_score(self, value):
        if not 0 <= value <= 10:
            raise serializers.ValidationError('A nota deve estar entre 0 e 10')
        return value
        