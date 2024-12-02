from django.db.models import Count, Case, When, Avg, Q
from achievement.models import UserProgress, PerformanceAnalytics
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
def get_specific_info(course):
    ''' Return number of enrollments, Average score, Pass rate of 1 course'''
    enrollments = Enrollment.objects.filter(course=course)
    enrollment_count = enrollments.count()

    average_score = enrollments.aggregate(
        avg_score=Avg('course__performanceanalytics__score', filter=Q(student__performanceanalytics__score__isnull=False))
    )['avg_score']

    # pass_count = enrollments.filter(student__userprogress__progress_percentage=100).count()
    pass_count = UserProgress.objects.filter(course=course,progress_percentage=100).count()

    pass_rate = round((pass_count / enrollment_count) * 100,2) if enrollment_count > 0 else 0

    return {
        'enrollment_count': enrollment_count,
        'average_score': round(average_score,2) if average_score is not None else 0,
        'pass_rate': pass_rate
    }

def get_score_distribution(course):
    ''' Get score distribution of specific course'''
    # Truy vấn và tính toán số lượng điểm trong từng khoảng
    score_distribution = PerformanceAnalytics.objects.filter(course=course).aggregate(
        range_0_10   = Count(Case(When(score__gte=0, score__lt=10, then=1))),
        range_10_20  = Count(Case(When(score__gte=10, score__lt=20, then=1))),
        range_20_30  = Count(Case(When(score__gte=20, score__lt=30, then=1))),
        range_30_40  = Count(Case(When(score__gte=30, score__lt=40, then=1))),
        range_40_50  = Count(Case(When(score__gte=40, score__lt=50, then=1))),
        range_50_60  = Count(Case(When(score__gte=50, score__lt=60, then=1))),
        range_60_70  = Count(Case(When(score__gte=60, score__lt=70, then=1))),
        range_70_80  = Count(Case(When(score__gte=70, score__lt=80, then=1))),
        range_80_90  = Count(Case(When(score__gte=80, score__lt=90, then=1))),
        range_90_100 = Count(Case(When(score__gte=90, score__lte=100, then=1))),
    )

    # Chuyển đổi kết quả sang định dạng phù hợp cho frontend
    distribution = {
        "ranges": ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"],
        "counts": [
            score_distribution["range_0_10"],
            score_distribution["range_10_20"],
            score_distribution["range_20_30"],
            score_distribution["range_30_40"],
            score_distribution["range_40_50"],
            score_distribution["range_50_60"],
            score_distribution["range_60_70"],
            score_distribution["range_70_80"],
            score_distribution["range_80_90"],
            score_distribution["range_90_100"],
        ],
    }
    return distribution
    

from django.db.models import F

def get_score_completion_data(course_id):
    # Lấy dữ liệu từ database
    data = (
        PerformanceAnalytics.objects.filter(course_id=course_id)
        .exclude(completion_rate=None)  # Loại bỏ giá trị None
        .exclude(score=None)  # Loại bỏ giá trị None
        .values("score", "completion_rate")
    )
    return list(data)  # Trả về danh sách các điểm và tỷ lệ hoàn thành