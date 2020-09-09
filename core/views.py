from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F

from .models import Question, Choice


def index(request):
    last_questions_list = Question.objects.order_by('-date_published')[:5]
    context = {'last_questions_list': last_questions_list}
    return render(request, 'core/polls_list.html', context)


def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'core/poll_detail.html', {'question': question})


def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'core/poll_detail.html', {
            'question': question,
            'error_message': 'You didn\'t select a choice.'
        })
    else:
        # F() has the database - rather than Python - update a field’s value, avoiding a race condition.
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Return an HttpResponseRedirect
        return HttpResponseRedirect(reverse('core:poll_result', args=(question.id,)))


def results(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'core/poll_result.html', {'question': question})
