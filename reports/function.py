from achievement.models import UserProgress
from course.models import Enrollment

def cleaned_data(query:str):
    ''' Get all characters before '-' '''
    query = query.strip()
    query = query[:query.find('-')] if '-' in query else query
    return query.strip()
def get_course_progress_and_enrollments(courses):
    ''' Get course number of enrollment and percent of progress '''
    num_enrollments = []
    num_passes = []
    course_code = [course.course_code for course in courses]
    course_name = [course.course_name for course in courses]
    for course in courses:
        num_enrollment = Enrollment.objects.filter(course=course).count()
        num_pass = UserProgress.objects.filter(course=course,progress_percentage=100).count()

        num_enrollments.append(num_enrollment)
        num_passes.append(num_pass)

        # print(course.course_name, num_enrollment ,num_pass)
    return course_code, course_name, num_enrollments, num_passes

def get_highest_percent_pass(courses):
    ''' Get course which has highest pass percent'''
    output = {
        'highest': 0,
        'course_name': '',
        'num_pass': 0,
        'in_progress':0,
    }
    for course in courses:
        num_enrollment = Enrollment.objects.filter(course=course).count()
        num_pass = UserProgress.objects.filter(course=course,progress_percentage=100).count()
        percent = num_pass / num_enrollment if num_enrollment > 0 else 0
        if percent > output['highest']:
            output['highest'] = percent
            output['course_name'] = course.course_name
            output['num_pass'] = num_pass
            output['in_progress'] = num_enrollment - output['num_pass']
    return output

def get_lowest_percent_pass(courses):
    ''' Get course which has lowest pass percent'''
    output = {
        'lowest': 100,
        'course_name': '',
        'num_pass': 0,
        'in_progress':0,
    }
    for course in courses:
        num_enrollment = Enrollment.objects.filter(course=course).count()
        num_pass = UserProgress.objects.filter(course=course,progress_percentage=100).count()
        percent = num_pass / num_enrollment if num_enrollment > 0 else 0
        if percent < output['lowest'] and percent > 0:
            output['lowest'] = percent
            output['course_name'] = course.course_name
            output['num_pass'] = num_pass
            output['in_progress'] = num_enrollment - output['num_pass']

        if (percent == 0) and (num_enrollment > output['num_pass']+output['in_progress']):
            output['lowest'] = percent
            output['course_name'] = course.course_name
            output['num_pass'] = num_pass
            output['in_progress'] = num_enrollment - output['num_pass']
    return output


