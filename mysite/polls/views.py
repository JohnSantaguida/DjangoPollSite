from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
# Create your views here.


class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name='polls/details.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {'question':question,'error_message':"You didn't select a choice"})
    else:
        selected.votes+=1
        selected.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
