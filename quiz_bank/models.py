from django.db import models
from course.models import Course

# Create your models here.
class Chapter(models.Model):
    chapter_name = models.CharField(max_length=255)

    def __str__(self):
        return self.chapter_name

    class Meta:
        db_table = 'Chapter'
        indexes = [
            models.Index(fields=['chapter_name'])
        ]

    def save(self, *args, **kwargs):
        val = getattr(self, 'chapter_name', False)
        if val:
            setattr(self, 'chapter_name', val.strip())
        super(QuizBank, self).save(*args, **kwargs)

class QuizBank(models.Model):
    """_summary_
    This django model is used for saving questions.\n

    """    
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('TEXT', 'Text Response'),
    ]
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, default='MCQ')
    points = models.IntegerField()

    class Meta:
        db_table = 'QuizBank'
        indexes = [
            models.Index(fields=['question_type'])
        ]

    def save(self, *args, **kwargs):
        val = getattr(self, 'question_text', False)
        if val:
            setattr(self, 'question_text', val.strip())
        super(QuizBank, self).save(*args, **kwargs)

class Answer(models.Model):
    """_summary_
    This django model is used for saving answers according to their question
    """    
    question = models.ForeignKey(QuizBank, on_delete=models.CASCADE)
    option_text = models.TextField()
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'Answer'

    def __str__(self):
        return self.option_text
    
    def save(self, *args, **kwargs):
        val = getattr(self, 'option_text', False)
        if val:
            setattr(self, 'option_text', val.strip())
        super(Answer, self).save(*args, **kwargs)