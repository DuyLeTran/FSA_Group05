from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from collections import Counter
from course.models import Course, Enrollment
from assessments.models import Assessment, StudentAssessmentAttempt
from django.db.models import OuterRef, Subquery,Max
from user.models import User
from .ai_model import AIInsightModel
from course.models import Course, Enrollment,SessionCompletion,Session
from assessments.models import Assessment, StudentAssessmentAttempt,CourseFinalScore,AssessmentFinalScore
from django.db.models import OuterRef, Subquery,Max,F
from user.models import User

 
#########################################################################################################
class UserProgress(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # String reference to avoid circular import
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_accessed = models.DateTimeField(auto_now=True)  # Updated to reflect last accessed time

    class Meta:
        unique_together = ('user', 'course')
        db_table = 'achievement_progress'

    def __str__(self):
        return f"{self.user} - {self.course} - {self.progress_percentage}%"
    
def calculate(user_id, course_id):
    quizzes = Assessment.objects.filter(course=course_id).count()
    attempts = len(Counter(set(
        StudentAssessmentAttempt.objects.filter(user=user_id, assessment__course=course_id).values_list('assessment_id', flat=True)
        )))
    return quizzes, attempts

@receiver([post_save, post_delete], sender=Assessment)
def update_quiz_progress(sender, instance, **kwargs):

    enrollments = Enrollment.objects.filter(course=instance.course)
    for enrollment in enrollments:
        user_id = enrollment.student.id
        total, attempts = calculate(user_id, instance.course.id)
        
        percent = round(attempts / total * 100, 2) if total > 0 else 0
        
        progress, created = UserProgress.objects.get_or_create(
            user=enrollment.student,
            course=instance.course
        )
        progress.progress_percentage = percent
        progress.save()

@receiver([post_save, post_delete], sender=StudentAssessmentAttempt)
def update_user_progress(sender, instance, **kwargs):
    try:
        user_id = instance.user.id
        course_id = instance.assessment.course.id
        total, attempts = calculate(user_id, course_id)

        percent = round(attempts / total * 100, 2) if total > 0 else 0
        
        progress, _ = UserProgress.objects.get_or_create(
            user=instance.user,
            course=instance.assessment.course
        )
        progress.progress_percentage = percent
        progress.save()
    except: pass

@receiver([post_save, post_delete], sender=Enrollment)
def update_enrollment_progress(sender, instance, **kwargs):
    if kwargs.get('created', False):  # Sự kiện post_save
        user_id = instance.student.id
        course_id = instance.course.id
        total, attempts = calculate(user_id, course_id)
        
        percent = round(attempts / total * 100, 2) if total > 0 else 0
    
        progress, _ = UserProgress.objects.get_or_create(
            user=instance.student,
            course=instance.course
        )
        progress.progress_percentage = percent
        progress.save()
    else:  # Sự kiện post_delete
        user_id = instance.student.id
        course_id = instance.course.id
        UserProgress.objects.filter(user=instance.student, course=instance.course).delete()
#########################################################################################################
class PerformanceAnalytics(models.Model):
     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField(default=0) 
    completion_rate = models.FloatField(default=0.0, null=True, blank=True)
    
    def update(self):
        assessments = Assessment.objects.filter(course=self.course)
        total_sessions = Session.objects.filter(course=self.course).count()
        completed_sessions = SessionCompletion.objects.filter(session__course=self.course, user=self.user, completed=True).count()
        total_assessments = Assessment.objects.filter(course=self.course).count()
        for assessment in assessments:
            qualifying_score = assessment.qualify_score
            completed_assessments = AssessmentFinalScore.objects.filter(
                    assessment__course=self.course,
                    user=self.user
                ).annotate(
                    total_score=F('final_score_ass') + F('final_score_quiz')
                ).filter(
                    total_score__gte=qualifying_score
                ).count()

        self.completion_rate = round(((completed_sessions + completed_assessments)/ (total_sessions + total_assessments)) * 100, 2) if total_sessions > 0 else 0
        highest_score = CourseFinalScore.objects.filter(user=self.user, course=self.course).aggregate(Max('score'))['score__max']
            
        self.score = highest_score or 0
            
        
        self.save()
    class Meta:
        db_table ='achievement_performance'
@receiver([post_delete,post_save],sender = CourseFinalScore)
def update_analytics(sender, instance, **kwargs):
    
        performance,created =PerformanceAnalytics.objects.get_or_create(
            user = instance.user,
            course = instance.course
        )  
        performance.update()      
    
        

@receiver([post_save,post_delete],sender = StudentAssessmentAttempt)
def update_analytics(sender, instance, **kwargs):
    
        performance,created =PerformanceAnalytics.objects.get_or_create(
            user = instance.user,
            course = instance.assessment.course
        )  
        performance.update()
    


@receiver(post_save, sender=Enrollment)
def create_performance(sender, instance, created, **kwargs):
    if created:
        PerformanceAnalytics.objects.create(
            user=instance.student,
            course=instance.course
        )

@receiver(post_delete, sender=Enrollment)
def delete_performance(sender, instance, **kwargs):
    try:
        performance = PerformanceAnalytics.objects.get(
            user=instance.student,
            course=instance.course
        )
        performance.delete()
    except PerformanceAnalytics.DoesNotExist:
        pass
#########################################################################################################
class AIInsights(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    insight_text = models.CharField(max_length=255, blank=True, null=True)
    insight_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.course} - {self.insight_text} - {self.insight_type}"
    
    def save(self, *args, **kwargs):
        for fields in ['insight_text', 'insight_type']:
            val = getattr(self, fields, False)
            if val:
                setattr(self, fields, val.capitalize().strip())
        super(AIInsights, self).save(*args, **kwargs)

@receiver(post_save, sender=Enrollment)
def update_insight_on_enrollment(sender, instance, created, **kwargs):
    AIInsights.objects.update_or_create(
        user=instance.student,
        course=instance.course,
        insight_type=None,
        insight_text=None,
    )

@receiver(post_delete, sender=Enrollment)
def delete_insight_on_enrollment_delete(sender, instance, **kwargs):
    AIInsights.objects.filter(
        user=instance.student,
        course=instance.course,
    ).delete()

@receiver(post_save, sender=StudentAssessmentAttempt)
def create_insight_on_assessment_attempt(sender, instance, **kwargs):
    try:
        student_assessments = StudentAssessmentAttempt.objects.filter(
            user = instance.user,
            assessment__course__id=instance.assessment.course.id
        )
        score_history = []
        count = 1
        for student_assessment in student_assessments:
            score_history.append(f"{student_assessment.score_quiz}")
            count += 1

        score = instance.score_quiz
        insight_text, insight_type = AIInsightModel(score,score_history)

        AIInsights.objects.create(
            user=instance.user,
            course=instance.assessment.course,
            insight_type=insight_type,
            insight_text=insight_text,
        )
    except: pass
