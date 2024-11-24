from django.shortcuts import render, HttpResponse
from module_group.models import ModuleGroup, Module
from activity.models import UserActivityLog
from django.db.models import Count, Q
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render
from course.models import Course, Session
from django.core.paginator import Paginator

module_groups = ModuleGroup.objects.all()
modules = Module.objects.all()

def user_perform_report(request): 
    return render(request, 'achievement/user_perform_report.html', {'module_groups': module_groups,
                                                           'modules': modules,})
def course_perform_report(request): 
    return render(request, 'achievement/course_perform_report.html', {'module_groups': module_groups,
                                                           'modules': modules,})
def risk_prediction_report(request):
    courses = Course.objects.values_list('course_name', flat=True)

    course_activity_counts = {}
    for course_name in courses:
        course_filter = Q(activity_details__icontains=course_name)

        user_activity_counts = UserActivityLog.objects.filter(
            course_filter
        ).values('user__username').annotate(activity_count=Count('log_id')).order_by('-activity_count')

        if user_activity_counts.exists():
            course_activity_counts[course_name] = list(user_activity_counts)

    evaluation_report = []
    for course_name, course_data in course_activity_counts.items():
        session_count = Session.objects.filter(course__course_name=course_name).count()
        for user_data in course_data: 
            user = user_data['user__username']
            activity_count = user_data['activity_count']
            evaluation_report.append({
                'course_name': course_name,
                'user': user,
                'activity_count': activity_count,
                'session_count': session_count, 
            })
    data = {}

    for entry in evaluation_report:
        course_name = entry['course_name']
        activity_count = entry['activity_count']  
        session_count = entry['session_count']

        if course_name not in data:
            data[course_name] = [0, 0, 0]  

        if activity_count < (session_count):
            data[course_name][2] += 1
        elif (session_count) <= activity_count <= (session_count*2):
            data[course_name][1] += 1
        else:
            data[course_name][0] += 1

    
    labels = ['Low', 'Medium', 'High']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(list(data.items()), 8)  # 4 items per page
    paginated_data = paginator.get_page(page)

    context = {
        'evaluation_report': evaluation_report,
        'labels': labels,
        'data': dict(paginated_data),
        'paginator': paginator,
        'paginated_data': paginated_data,
        'module_groups': module_groups,
        'modules': modules,
    }

    return render(request, 'achievement/risk_prediction_report.html', context)



def student_risk_predict(request, course_name):
    course = Course.objects.get(course_name=course_name)
    session_count = Session.objects.filter(course=course).count()
    user_activity_counts = UserActivityLog.objects.filter(
        activity_details__icontains=course_name
    ).values('user__username').annotate(activity_count=Count('log_id')).order_by('-activity_count')

    data =[0,0,0]
    for user_data in user_activity_counts:
        activity_count = user_data['activity_count']
        if activity_count < session_count:
            user_data['risk'] = 'High'
            data[2] += 1
        elif session_count <= activity_count <= session_count*2:
            user_data['risk'] = 'Medium'
            data[1] += 1

        else:
            user_data['risk'] = 'Low'
            data[0] += 1

    labels = ['Low', 'Medium', 'High']
    paginator = Paginator(user_activity_counts, 10) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'achievement/risk_report.html', {
        'course': course,
        'user_activity_counts': user_activity_counts,
        'activity_count': activity_count,
        "data": data,
        'labels': labels,
        'page_obj': page_obj,
        'module_groups': module_groups,
        'modules': modules,

    })




