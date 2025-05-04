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
        if scores.exists():
            return sum(s.score for s in scores) / scores.count()
        return 0

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.score}"
