from django import forms
from course.models import Course
from quiz.models import Question, Quiz, AnswerOption
from .models import QuizBank, Answer, Chapter
from django.forms.models import inlineformset_factory

class QuestionCourseForm(forms.ModelForm):
    question_type = forms.ChoiceField(choices=[('MCQ', 'MCQ'), ('TF', 'TF'), ('TEXT', 'TEXT')],
                                      required=False)
    class Meta:
        model = Quiz
        fields = ['course']
        labels = {
            'course': 'Select a Course:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()

class ExcelImportForm(forms.ModelForm):
    question_type = forms.ChoiceField(choices=[('MCQ', 'MCQ'), ('TF', 'TF'), ('TEXT', 'TEXT')],
                                      required=False)
    class Meta:
        model = Quiz
        fields = ['course']
        labels = {
            'course': 'Select a Course:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()

class QuestionTypeForm(forms.Form):
    question_type = forms.ChoiceField(choices=[('MCQ', 'MCQ'), ('TF', 'TF'), ('TEXT', 'TEXT')])

class NumberForm(forms.Form):
    number_of_questions = forms.IntegerField(label="Enter Number of Questions")
    question_type = forms.ChoiceField(choices=[('MCQ', 'MCQ'), ('TF', 'TF'), ('TEXT', 'TEXT')],
                                      required=False)

class FilterByQuestionTypeForm(forms.Form):
    filter_by = forms.ChoiceField(choices=[('MCQ', 'MCQ'), ('TF', 'TF'), ('TEXT', 'TEXT')])
    chapter = forms.ChoiceField(choices=[('all', 'All'), *tuple((_chapter.chapter_name, _chapter.chapter_name) for _chapter in Chapter.objects.all())], required=False)

class ExportTypeForm(forms.Form):
    export_type = forms.ChoiceField(choices=[('JSON', 'JSON'), ('EXCEL', 'EXCEL')])

class SearchByCourseForm(forms.Form):
    search_by = forms.CharField(
        label="Search course (code/name):",
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'list': 'course_list'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        # courses = kwargs.pop('courses', [])
        super().__init__(*args, **kwargs)
        self.fields['search_by'].widget.attrs['datalist'] = 'course_list'
        # self.fields['search_by'].widget.choices = [(course.course_name, course.course_name) for course in courses] + [(course.course_code, course.course_code) for course in courses]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['option_text', 'is_correct']
        labels = {
            'is_correct': 'Correct Answer:'
        }
        widgets = {
            'is_correct': forms.CheckboxInput(),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuizBank
        fields = ['question_text', 'chapter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chapter'].queryset = Chapter.objects.all()

class QuestionAddForm(forms.ModelForm):
    class Meta:
        model = QuizBank
        fields = ['question_text', 'question_type', 'points', 'chapter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chapter'].queryset = Chapter.objects.all()

class ExcelImportWithoutCourseForm(forms.Form):
    excel_file = forms.FileField(label="Upload Excel File")
    question_type = forms.ChoiceField(choices=[('MCQ', 'MCQ'), ('TF', 'TF'), ('TEXT', 'TEXT')],
                                      required=False)

class NumberOfQuestionsForm(forms.Form):
    number_of_questions = forms.IntegerField(label="Enter Number of Questions", required=False)

class GetRandomForm(forms.ModelForm):
    number_of_questions = forms.IntegerField(label="Enter Number of Questions", required=False)
    class Meta:
        model = Quiz
        fields = ['course']
        labels = {
            'course': 'Select a Course:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()

class JSONForm(forms.Form):
    json_file = forms.FileField(label='Upload JSON')

AnswerOptionFormset = inlineformset_factory(
    parent_model=QuizBank,
    model=Answer,
    form=AnswerForm,
    extra=0,  # Adjust 'extra' to control initial empty forms
)

QuestionFormset = inlineformset_factory(
    parent_model=Course,
    model=QuizBank,
    form=QuestionForm,
    formset=AnswerOptionFormset,
    extra=0,  # Adjust 'extra' to control initial empty forms
)