from django.urls import path, re_path
from django.views.generic import TemplateView
from catalogue import views

# app_name = 'polls'
urlpatterns = [

    path('polls/', views.index, name='index'),
    # ex: /polls/5/
    path('polls/<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('polls/<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('polls/<int:question_id>/addchoice/', views.ChoiceCreate.as_view(), name='choice-create'),
    path('polls/addquestion/', views.QuestionCreate.as_view(), name='question-create'),
    path('polls/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),

]


