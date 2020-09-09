from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question


def index(request):
    last_questions_list = Question.objects.order_by('-date_published')[:5]
    context = {'last_questions_list': last_questions_list}
    return render(request, 'core/polls_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse(f'You are looking at the results of question {question_id}')


def vote(request, question_id):
    return HttpResponse(f'You are looking at the vote of question {question_id}')
