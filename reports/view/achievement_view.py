from django.shortcuts import render, HttpResponse
from django.db.models import Count, F, Q
from module_group.models import ModuleGroup, Module
from ..forms import CourseForm
from ..function import cleaned_data, get_course_progress_and_enrollments, get_highest_percent_pass, get_lowest_percent_pass
from course.models import Course
from django.db.models import Q
from course.models import Enrollment

module_groups = ModuleGroup.objects.all()
modules = Module.objects.all()

def user_perform_report(request): 
    return render(request, 'achievement/user_perform_report.html', {'module_groups': module_groups,
                                                           'modules': modules,})


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

