from django import forms

class CourseForm(forms.Form):
    course = forms.CharField(label = 'Search')