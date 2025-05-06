from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    @property
    def average_overall(self):
        scores = self.score_set.all()
        if scores:
            return sum(score.score for score in scores) / len(scores)
        return 0
    
    def average_subject(self, subject):
        scores = self.score_set.select_related('subject').filter(subject=subject)
        if scores.count() == 4:
            return sum(s.score for s in scores) / 4
        return 0

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Score(models.Model):
    BIMESTER_CHOICES = [
        (1, '1º Bimestre'),
        (2, '2º Bimestre'),
        (3, '3º Bimestre'),
        (4, '4º Bimestre'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.PositiveSmallIntegerField(choices=BIMESTER_CHOICES, default=1)
    score = models.FloatField()

    class Meta:
        unique_together = ['student', 'subject', 'term']

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.score}"
