from .models import Student, Subject, Score
from rest_framework import serializers
from collections import defaultdict
from django.db import IntegrityError

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','name']

class ScoreSerializer(serializers.ModelSerializer):    
    student_name = serializers.CharField(source='student.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Score
        fields = ['id','student', 'subject', 'score', 'student_name', 'subject_name']

    def validate_score(self, value):
        if not 0 <= value <= 10:
            raise serializers.ValidationError('A nota deve estar entre 0 e 10')
        return value
    
    def validate(self, data):
        student = data.get('student')
        subject = data.get('subject')
        term = data.get('term')

        if Score.objects.filter(student=student, subject=subject, term=term).exists():
            raise serializers.ValidationError('Já existe uma nota para esse aluno nesse bimestre')
        
        return data
    
    def create(self, validated_data):
        try:
            score = Score.objects.create(**validated_data)
            return score
        except IntegrityError:
            raise serializers.ValidationError('Já existe uma nota para esse aluno nesse bimestre')

    def update(self, instance, validated_data):
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'average_overall', 'subjects']

    def get_subjects(self, student):
        data = defaultdict(list)

        for score in student.score_set.select_related('subject'):
            data[score.subject.name].append({
                'term': score.term,
                'score': score.score,
            })

        for scores in data.values():
            scores.sort(key=lambda s: s['term'])

        result = []
        for subject_name, scores in data.items():
            subject = Subject.objects.get(name=subject_name)
            everage = student.average_subject(subject)
            result.append({
                'subject': subject_name,
                'scores': scores,
                'everage': everage
            })
        
        return result
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('view').action == 'retrieve':
            return representation
        else:
            representation.pop('subjects', None)
            return representation
