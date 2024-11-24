from django.shortcuts import render, HttpResponse
from django.db.models import Count, F, Q
from module_group.models import ModuleGroup, Module
from ..forms import CourseForm
from ..function import cleaned_data, get_course_progress_and_enrollments, get_highest_percent_pass, get_lowest_percent_pass
from course.models import Course
from django.db.models import Q
from course.models import Enrollment
from module_group.models import ModuleGroup, Module
from user.models import User
from course.models import Course,Enrollment,SessionCompletion,Session,Completion
from django.db.models import Count, Sum, Avg, F, Q, Max, Subquery, OuterRef, Min
from assessments.models import StudentAssessmentAttempt, Assessment,CourseFinalScore

module_groups = ModuleGroup.objects.all()
modules = Module.objects.all()

def course_perform_report(request):
    all_courses = Course.objects.all()
    form = CourseForm(request.GET)
    if form.is_valid() and form.cleaned_data['course'] != 'All': 
        searched = cleaned_data(form.cleaned_data['course'])  # course is variable of CourseForm
        course = Course.objects.filter(Q(course_code=searched) | Q(course_name=searched))
        if not course.first():
            message = 'Invalid Course'
            return render(request, 'achievement/course_perform_report.html', {'module_groups': module_groups,
                                                           'modules': modules,
                                                           'form': form,
                                                           'message': message,
                                                           'all_courses':all_courses,})
        else:
            display = 'specific'
            
            return render(request, 'achievement/course_perform_report.html', {'module_groups': module_groups,
                                                           'modules': modules,
                                                           'form': form,
                                                           'all_courses':all_courses,
                                                           'display': display})
    else:
        display = 'All'

        course_enroll_count = Enrollment.objects.values('course').distinct().count() # Use for bar chart 'Comparison of Enrollment and Pass Counts Across Courses'

        context = {
                'course_enroll_count': course_enroll_count,
                'course_unenroll_count': all_courses.count()-course_enroll_count,
                # --------------------------------- Bar Chart ---------------------------------
                'course_code': get_course_progress_and_enrollments(all_courses)[0],
                'course_name': get_course_progress_and_enrollments(all_courses)[1],
                'enroll_counts': get_course_progress_and_enrollments(all_courses)[2],
                'pass_counts': get_course_progress_and_enrollments(all_courses)[3],

                # ---------------------- Pie Chart highest pass percent -----------------------
                'highest_pass_course_name':get_highest_percent_pass(all_courses)['course_name'],
                "pass_count_highest": get_highest_percent_pass(all_courses)['num_pass'],
                "in_progress_count_highest": get_highest_percent_pass(all_courses)['in_progress'],

                # ---------------------- Pie Chart highest lowest percent -----------------------
                'lowest_pass_course_name':get_lowest_percent_pass(all_courses)['course_name'],
                "pass_count_lowest": get_lowest_percent_pass(all_courses)['num_pass'],
                "in_progress_count_lowest": get_lowest_percent_pass(all_courses)['in_progress'],
            }

    return render(request, 'achievement/course_perform_report.html', {'module_groups': module_groups,
                                                           'modules': modules,
                                                           'form': form,
                                                           'all_courses':all_courses,
                                                           'display': display,
                                                           'context': context})

def user_perform_report(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query) if query else User.objects.all()
    all_usernames = User.objects.values_list('username', flat=True)
    user_data = []

    for user in users:
        user_enrollments = Enrollment.objects.filter(student=user.id)
        courses = []
        for user_enrollment in user_enrollments:
            course = user_enrollment.course
            course_completion_rate = Course.get_completion_percent(course, user)
            final_score = CourseFinalScore.objects.filter(course=course, user=user).first()
            courses.append({
                'course_name': course.course_name,
                'completion_rate': course_completion_rate,
                'final_score': final_score.score if final_score else 'N/A'
            })
        user_data.append({
            'user': user,
            'courses': courses
        })

    total_users = User.objects.count()
    users_enrolled = Enrollment.objects.values('student').distinct().count()
    enrollments_by_course = Enrollment.objects.values('course').distinct().count()

    
    # Prepare data for the pie chart
    courses = Course.objects.all()
    pie_chart_data = []
    for course in courses:
        enrollment_count = Enrollment.objects.filter(course=course).count()
        
        pie_chart_data.append({
                'name': course.course_name,
                'enrollment_count': enrollment_count
        })

    # Prepare data for score analysis
    score_analysis_data = []
    scores = []
    if query:
        user = users.first()
        user_enrollments = Enrollment.objects.filter(student=user)
        for user_enrollment in user_enrollments:
            course = user_enrollment.course
            avg_score = CourseFinalScore.objects.filter(course=course, user=user).exclude(score =0).aggregate(Avg('score'))['score__avg'] or 0
            highest_score = CourseFinalScore.objects.filter(course=course, user=user).aggregate(Max('score'))['score__max'] or 0
            lowest_score = CourseFinalScore.objects.filter(course=course, user=user).aggregate(Min('score'))['score__min'] or 0
            date_completed = CourseFinalScore.objects.filter(course=course, user=user).aggregate(Max('date'))['date__max']
            score_analysis_data.append({
                'name': course.course_name,
                'avg_score': avg_score,
                'highest_score': highest_score,
                'lowest_score': lowest_score,
                'date_completed': date_completed
            })
            if avg_score !=0:
                scores.append(avg_score)

    avg_score = sum(scores) / len(scores) if scores else 0
    highest_score = max([data['highest_score'] for data in score_analysis_data]) if score_analysis_data else 0
    lowest_score = min([data['lowest_score'] for data in score_analysis_data]) if score_analysis_data else 0

    context = {
        'user_data': user_data,
        'query': query,
        'all_usernames': all_usernames,
        'total_users': total_users,
        'users_enrolled': users_enrolled,
        'enrollments_by_course': enrollments_by_course,
        'pie_chart_data': pie_chart_data,
        'score_analysis_data': score_analysis_data,
        'avg_score': avg_score,
        'highest_score': highest_score,
        'lowest_score': lowest_score,
    }

    return render(request, 'achievement/user_perform_report.html', context)
