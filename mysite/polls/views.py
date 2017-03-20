from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from . import models

# def index(request):
#     latest_questions = models.Question.objects.order_by('-pub_date')[:5]
#     response = render(request, 'polls/index.html', {'latest_questions': latest_questions})
#     return response

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        """
        Return the last five published questions,
        excluding those that are to be published in the future
        """
        return models.Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def detail(request, question_id):
#     question = get_object_or_404(models.Question, pk=question_id)
#     response = render(request, 'polls/detail.html', {'question': question})
#     return response

class DetailView(generic.DetailView):
    model = models.Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Exclude any questions that aren't published yet.
        """
        return models.Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = models.Question
    template_name = 'polls/results.html'

# def results(request, question_id):
#     question = get_object_or_404(models.Question, pk=question_id)
#     response = render(request, 'polls/results.html', {'question': question})
#     return response

def vote(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, models.Choice.DoesNotExist):
        response = render(
            request,
            'polls/detail.html',
            {
                'question': question,
                'error_message': 'You didn\'t select a choice.'
            }
        )
        return response
    else:
        selected_choice.votes += 1
        selected_choice.save()
        response = HttpResponseRedirect(reverse('polls:results', args=[question.id]))
        return response