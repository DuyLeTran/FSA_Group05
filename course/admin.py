from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Course, Session, Topic, Tag
from user.models import User
from .models import CourseMaterial, ReadingMaterial
from import_export.fields import Field

class CourseResource(resources.ModelResource):
    creator = fields.Field(
        attribute='creator',
        column_name='creator__username',
        widget=ForeignKeyWidget(User, 'username')
    )
    instructor = fields.Field(
        attribute='instructor',
        column_name='instructor__username',
        widget=ForeignKeyWidget(User, 'username')
    )
    prerequisites = fields.Field(
        attribute='prerequisites',
        column_name='prerequisites',
        widget=ManyToManyWidget(Course, field='course_name', separator='|')
    )
    tags = fields.Field(
        attribute='tags',
        column_name='tags',
        widget=ManyToManyWidget(Tag, field='name', separator='|')
    )

    class Meta:
        model = Course
        fields = (
            'course_name',
            'course_code',
            'description',
            'creator',
            'instructor',
            'published',
            'prerequisites',
            'tags',
        )
        import_id_fields = ('course_name',)

    def after_import(self, dataset, result, **kwargs):
        for row in dataset.dict:
            course_name = row['course_name']
            try:
                # Get the course by name
                course = Course.objects.get(course_name=course_name)

                # Process prerequisites after the course has been saved
                if row.get('prerequisites'):
                    prerequisites = row['prerequisites'].split('|')
                    for prereq_name in prerequisites:
                        prereq_name = prereq_name.strip()
                        if prereq_name:
                            # Find or create the prerequisite course using course_name
                            prereq_course, _ = Course.objects.get_or_create(course_name=prereq_name)
                            # Add the prerequisite to the course
                            course.prerequisites.add(prereq_course)
            except Course.DoesNotExist:
                print(f"Course '{course_name}' does not exist.")  # Handle missing courses

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin
from .models import Session, Course

class SessionResource(resources.ModelResource):
    course = fields.Field(
        attribute='course', 
        column_name='course__course_name',
        widget=ForeignKeyWidget(Course, 'course_name')
    )
    
    class Meta:
        model = Session
        fields = ('id', 'course', 'name', 'order')
        import_id_fields = ('id',)

    def before_import_row(self, row, **kwargs):
        course_name = row.get("course__course_name")
        if course_name:
            try:
                # Check if course exists
                Course.objects.get(course_name=course_name)
            except Course.DoesNotExist:
                # Optionally, skip or log the row
                row['import_error'] = f"Course '{course_name}' does not exist."

@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    resource_class = SessionResource
    list_display = ('course', 'name', 'order')
    search_fields = ('course__course_name', 'name')


class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        fields = ('id', 'name')  # Add any additional fields you want to include
        import_id_fields = ('id',)

class TagResource(resources.ModelResource):
    topic = fields.Field(attribute='topic', column_name='topic__name', widget=ForeignKeyWidget(Topic, 'name'))

    class Meta:
        model = Tag
        fields = ('id', 'name', 'topic')  # Include any other relevant fields
        import_id_fields = ('id',)


class ReadingMaterialResource(resources.ModelResource):
    material_id = Field(attribute='material', column_name='material_id')

    class Meta:
        model = ReadingMaterial
        fields = ('id', 'material_id', 'title')  # Include 'id' if you want to allow updating existing entries
        import_id_fields = ('id',)  # Use this to identify existing records based on 'id'


class ReadingMaterialResource(resources.ModelResource):
    material_id = fields.Field(
        attribute='material',
        column_name='material_id',
        widget=ForeignKeyWidget(CourseMaterial, 'id')
    )
    content = fields.Field(
        attribute='content',
        column_name='content'
    )

    class Meta:
        model = ReadingMaterial
        fields = ('id', 'material_id', 'title', 'content')  # Include 'content' here
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        # Check if material_id exists in CourseMaterial
        if not CourseMaterial.objects.filter(id=row.get('material_id')).exists():
            row['material_id'] = None  # Set to None if material_id doesn't exist

@admin.register(ReadingMaterial)
class ReadingMaterialAdmin(ImportExportModelAdmin):
    resource_class = ReadingMaterialResource
    list_display = ('material', 'title', 'content')  # Added 'content' to display it in the admin list
    search_fields = ('title', 'material__title', 'content')  # Include 'content' in search fields

    # Optional: If 'content' field is too long to display, consider using a truncated version for readability:
    def truncated_content(self, obj):
        return obj.content[:50] + "..." if obj.content and len(obj.content) > 50 else obj.content

    truncated_content.short_description = 'Content'

    list_display = ('material', 'title', 'truncated_content')  # Replaced 'content' with truncated version
    
# Course
from import_export import resources, fields, widgets


class CourseMaterialResource(resources.ModelResource):
    # Using ForeignKeyWidget to handle the session foreign key relationship
    session_id = fields.Field(
        column_name='session_id',
        attribute='session',
        widget=widgets.ForeignKeyWidget(Session, 'id')
    )

    class Meta:
        model = CourseMaterial
        fields = ('id', 'session_id', 'material_id', 'material_type', 'order', 'title')
        import_id_fields = ('id',)

@admin.register(CourseMaterial)
class CourseMaterialAdmin(ImportExportModelAdmin):
    resource_class = CourseMaterialResource
    list_display = ('session', 'material_id', 'material_type', 'order', 'title')
    search_fields = ('title', 'session__id')


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ('course_name', 'course_code', 'published')
    list_per_page = 5
    search_fields = ('course_name', 'course_code')
    list_filter = ('published',)



@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin):
    resource_class = TopicResource
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    resource_class = TagResource
    list_display = ('name', 'topic')
    search_fields = ('name', 'topic__name')

