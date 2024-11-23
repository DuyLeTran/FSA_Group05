from django.urls import path
from . import views

app_name = 'student_portal'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('enroll/<int:pk>/', views.enroll, name='enroll'),
    path('<int:pk>/unenroll/', views.unenroll, name='unenroll'),
    path('instructor/<int:instructor_id>/', views.instructor_profile, name='instructor_profile'),
    
]



