from django.urls import path
from .views import bank_request_views\
                  ,export_request_views\
                  ,question_request_views\
                  ,import_request_views\
                  ,json_modifier_views

app_name = 'quiz_bank'

urlpatterns = [
    path('', bank_request_views.quiz_bank_view, name='quiz_bank_view'),
    path('refresh/', bank_request_views.quiz_bank_view_refresh, name='quiz_bank_view_refresh'),
    path('show/<int:course_id>/', bank_request_views.quiz_bank_course, name='quiz_bank_course'),
    path('show/<int:course_id>/refresh', bank_request_views.quiz_bank_course_refresh, name='quiz_bank_course_refresh'),
    path('delete_selection/<int:course_id>/', question_request_views.delete_selected_question, name='delete_selected_question'),
    path('delete_selection/<int:course_id>/confirm/', question_request_views.delete_selected_confirm, name='delete_selected_confirm'),
    path('add_question/<int:course_id>/', question_request_views.add_question, name='add_question'),
    path('edit_question/<int:course_id>/', question_request_views.edit_multiple_question, name='edit_multiple_question'),

    path('random/', bank_request_views.random_question_before_add_quiz, name='random_question_before_add_quiz'),
    path('random/refresh/<int:course_id>/<int:number_of_questions>', bank_request_views.random_question_refresh, name='random_question_refresh'),
    path('random/<int:course_id>/<int:number_of_questions>', bank_request_views.random_question_view, name='random_question_view'),
    path('show/<int:course_id>/delete/<int:question_id>', question_request_views.delete_question, name='delete_question'),
    path('show/<int:course_id>/edit/<int:question_id>', question_request_views.edit_question, name='edit_question'),
    path('import/', import_request_views.import_quiz_bank, name='import_quiz_bank'),
    path('show/<int:course_id>/import/', import_request_views.import_quiz_bank_from_page, name='import_quiz_bank_from_page'),
    path('export_selection/<int:course_id>/', export_request_views.export_selected_question, name='export_selected_question'),
    path('export_selection/<int:course_id>/confirm/', export_request_views.export_selected_confirm, name='export_selected_confirm'),

    path('json/upload/', json_modifier_views.json_upload, name='json_upload'),
    path('json/modify/', json_modifier_views.json_modification, name='json_modification'),
    path('json/delete/<int:question_id>', json_modifier_views.json_delete_question, name='json_delete_question'),
    path('json/edit/<int:question_id>', json_modifier_views.json_edit_question, name='json_edit_question'),
] 