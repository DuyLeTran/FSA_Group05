# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from course.models import Course, Enrollment, Session
from student_portal.models import RecommendedCourse
from django.contrib import messages
from feedback.models import CourseFeedback
import random
from django.utils import timezone  # for timestamp updates
from django.core.paginator import Paginator
from user.models import User

def instructor_profile(request, instructor_id):
    # Get the instructor based on the instructor ID
    instructor = get_object_or_404(User, id=instructor_id)

    # Get courses taught by this instructor
    courses = Course.objects.filter(instructor=instructor)

    # Get feedback for each course to calculate average ratings
    for course in courses:
        feedbacks = CourseFeedback.objects.filter(course=course)
        if feedbacks.exists():
            total_rating = sum(feedback.average_rating() for feedback in feedbacks)
            course.average_rating = total_rating / feedbacks.count()
        else:
            course.average_rating = None  # No feedback yet

    context = {
        'instructor': instructor,
        'courses': courses,
    }

    return render(request, 'instructor_profile.html', context)

def course_list(request):
    # Retrieve all published courses initially
    courses = Course.objects.filter(published=True)
    query = request.GET.get('q')
    
    # Filter courses based on search query if present
    if query:
        courses = courses.filter(Q(course_name__icontains=query) | Q(description__icontains=query))

    # Add average rating to each course
    for course in courses:
        feedbacks = course.coursefeedback_set.all()
        if feedbacks.exists():
            # Calculate the average rating using the average_rating method
            total_ratings = sum(feedback.average_rating() for feedback in feedbacks)
            course.average_rating = total_ratings / feedbacks.count()
        else:
            course.average_rating = 0.0  # Default to 0 if there are no feedbacks

    # Insert or update recommended courses based on search results
    for course in courses:
        recommended_course, created = RecommendedCourse.objects.get_or_create(
            course=course,
            user=request.user,  # Associate with the logged-in user
            defaults={'created_at': timezone.now()}  # Set default created_at only if new
        )
        
        # Update the timestamp if the recommendation already exists
        if not created:
            recommended_course.created_at = timezone.now()
            recommended_course.save()

    # Paging
    paginator = Paginator(courses, 6)  # Show 6 courses per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get top recommended courses to display
    recommended_courses = RecommendedCourse.objects.filter(course__published=True).order_by('-created_at')[:4] 

    # Render the course list with filtered and recommended courses
    return render(request, 'courses/course_list.html', {
        'courses': page_obj,
        'recommended_courses': [rc.course for rc in recommended_courses],
    })


def course_detail(request, pk):
    # Get the course based on the primary key (pk)
    course = get_object_or_404(Course, pk=pk)

    # Check enrollment status
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    users_enrolled_count = Enrollment.objects.filter(course=course).count()

    # Get all feedback related to the course
    feedbacks = CourseFeedback.objects.filter(course=course)

    # Calculate the course's average rating
    if feedbacks.exists():
        total_rating = sum(feedback.average_rating() for feedback in feedbacks)
        course_average_rating = total_rating / feedbacks.count()
    else:
        course_average_rating = None  # No feedback yet

    course_average_rating_star = course_average_rating * 100 / 5 if course_average_rating is not None else 0

    # Get prerequisites
    prerequisites = course.prerequisites.all()

    # Get sessions
    sessions = Session.objects.filter(course=course)
    session_count = sessions.count()

    # Get random tags
    all_tags = list(course.tags.all())
    random_tags = random.sample(all_tags, min(4, len(all_tags)))

    # Fetch the latest feedbacks
    latest_feedbacks = feedbacks.order_by('-created_at')[:5]

    # Instructor info
    instructor = course.instructor
    is_instructor = Course.objects.filter(instructor=request.user).exists()
    user_type = 'instructor' if is_instructor else 'student'

    enrolled_users = Enrollment.objects.filter(course=course).select_related('student')

    # Calculate progress for each enrolled user
    user_progress = [
        {
            'user': enrollment.student,
            'progress': course.get_completion_percent(enrollment.student)
        }
        for enrollment in enrolled_users
    ]

    context = {
        'course': course,
        'prerequisites': prerequisites,
        'is_enrolled': is_enrolled,
        'users_enrolled_count': users_enrolled_count,
        'course_average_rating_star': course_average_rating_star,
        'course_average_rating': course_average_rating,
        'feedbacks': feedbacks,
        'sessions': sessions,
        'session_count': session_count,
        'latest_feedbacks': latest_feedbacks,
        'tags': course.tags.all() if course.tags else [],
        'instructor': instructor,
        'user_type': user_type,
        'user_progress': user_progress,
        'random_tags': random_tags,
    }

    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll(request, pk):
    course = get_object_or_404(Course, id=pk)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"You have successfully enrolled in {course.course_name}.")
    return redirect('student_portal:course_detail', pk=course.id)

@login_required
def unenroll(request, pk):
    # Get the course based on the primary key (pk)
    course = get_object_or_404(Course, pk=pk)

    # Attempt to delete the enrollment for the current user
    enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
    
    if enrollment:
        enrollment.delete()
        messages.success(request, f"You have successfully unenrolled from {course.course_name}.")
    else:
        messages.warning(request, f"You are not enrolled in {course.course_name}.")

    return redirect('student_portal:course_detail', pk=course.pk)

# def course_list(request):
#     # Retrieve all published courses initially
#     courses = Course.objects.filter(published=True)
#     query = request.GET.get('q')
    
#     # Filter courses based on search query if present
#     if query:
#         courses = courses.filter(Q(course_name__icontains=query) | Q(description__icontains=query))
        
#         # Insert or update recommended courses based on search results
#         for course in courses:
#             recommended_course, created = RecommendedCourse.objects.get_or_create(
#                 course=course,
#                 user=request.user,  # Associate with the logged-in user
#                 defaults={'created_at': timezone.now()}  # Set default created_at only if new
#             )
            
#             # Update the timestamp if the recommendation already exists
#             if not created:
#                 recommended_course.created_at = timezone.now()
#                 recommended_course.save()

#     # Get top recommended courses to display
#     recommended_courses = RecommendedCourse.objects.filter(course__published=True).order_by('-created_at')[:3] 

#     # Render the course list with filtered and recommended courses
#     return render(request, 'courses/course_list.html', {
#         'courses': courses,
#         'recommended_courses': [rc.course for rc in recommended_courses],
#     })