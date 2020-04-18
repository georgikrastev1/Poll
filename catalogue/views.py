# import csv
from datetime import datetime
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
# from .forms import TicketQuantityForm, ShowingForm
# from .filters import MovieShowingFilter
# from .emails import send_mail
# from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
import json

from .models import Question, Choice
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

from GOSH.settings import EMAIL_HOST_USER
from emails.emails import send_mail
from django.core.exceptions import PermissionDenied


from django.utils import timezone


# class DiseaseListView(ListView):
#     """
#     Generates a list of Diseases available in the system.
#     """
#     model = Disease
#     template_name = 'catalogue/disease_list.html'
#     context_object_name = 'diseases'
#     paginate_by = 5
def moderator_or_author_only(user, object):
    if user != object.author and not user.groups.filter(name='administrator').exists():
        raise PermissionDenied()

def moderator_only(user, object):
    if user.groups.filter(name='administrator').exists():
        raise PermissionDenied()

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context={
        'latest_question_list':latest_question_list
    }
    return render(request,'catalogue/polls.html',context)

@login_required()
def detail(request, question_id):
    details=Question.objects.get(id=question_id)
    context={
        'question': details,
    }
    return render(request,'catalogue/polls_d.html',context)

@login_required()
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices=Choice.objects.filter(question=question_id) #https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html

    choice_texts = []
    choice_votes = []
    dictdata=[['Choice','Votes']] #important insert category names on top

    for choice in choices:
        merge=[]
        merge.append(choice.choice_text)
        merge.append(choice.votes)
        dictdata.append(merge)
    print(dictdata)

    context={
        'question': question,
        'array': json.dumps(dictdata),
        'title': 'Polls Results Page',
        'choice_texts': choice_texts,
        'choice_votes': choice_votes,
        'choice_colours': ['rgba(0, 209, 178, 0.55)'] * len(choices),
        'choice_border_colours': ['rgba(0, 209, 178, 0.9)'] * len(choices),
    }

    return render(request, 'catalogue/results.html', context)

@login_required()
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'catalogue/polls_d.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))

class ChoiceCreate(LoginRequiredMixin,CreateView):
    model=Choice
    fields=['choice_text']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.question = Question.objects.filter(id=self.kwargs['question_id']).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'question_id': self.kwargs['question_id']})

class QuestionCreate(LoginRequiredMixin,CreateView):
    model=Question
    fields=['question_text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.pub_date=datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Question
    success_message = 'Disease successfully deleted!!!!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(QuestionDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('index')